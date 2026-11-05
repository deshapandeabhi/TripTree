<?php
/**
 * TripTree contact & booking form handler.
 * Requires PHP hosting with mail() enabled (standard on cPanel / most Indian shared hosts).
 * Set the sender below to an address on your own domain so emails are not marked as spam.
 */

$TO_EMAIL   = 'booking@triptree.co.in';
$FROM_EMAIL = 'no-reply@triptree.co.in';
$SITE_NAME  = 'TripTree Website';

$PROPERTIES = [
    'bandipur-farmhouse' => 'Bandipur Farmhouse',
    'harangi-backwaters' => 'Harangi Backwaters',
    'masinagudi-estate'  => 'Masinagudi Estate',
    'mudumalai-estate'   => 'Mudumalai Estate',
    'not-sure'           => 'Not sure yet',
];

$isAjax = (isset($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest')
       || (isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false);

function respond($ok, $message, $isAjax) {
    if ($isAjax) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'message' => $message]);
    } elseif ($ok) {
        header('Location: ../thank-you.html', true, 303);
    } else {
        http_response_code(400);
        header('Content-Type: text/html; charset=utf-8');
        echo '<!DOCTYPE html><meta charset="utf-8"><title>Form error</title><p>'
           . htmlspecialchars($message) . '</p><p><a href="javascript:history.back()">Go back</a></p>';
    }
    exit;
}

function field($key, $max = 200) {
    $v = isset($_POST[$key]) ? trim((string) $_POST[$key]) : '';
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);   // block header injection
    return mb_substr(strip_tags($v), 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ../contact.html', true, 303);
    exit;
}

// Spam honeypot: real visitors never fill this hidden field
if (!empty($_POST['website'])) {
    respond(true, 'Thank you! We will get back to you shortly.', $isAjax);
}

$type    = field('form_type', 20) === 'booking' ? 'booking' : 'contact';
$name    = field('name', 100);
$email   = field('email', 150);
$phone   = field('phone', 20);
$subject = field('subject', 150);
$message = isset($_POST['message']) ? mb_substr(trim(strip_tags((string) $_POST['message'])), 0, 3000) : '';

if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || !preg_match('/^[0-9+()\- ]{7,20}$/', $phone)) {
    respond(false, 'Please enter your name, a valid email address and phone number.', $isAjax);
}

$lines = [];
if ($type === 'booking') {
    $propKey  = field('property', 40);
    $checkin  = field('checkin', 10);
    $checkout = field('checkout', 10);
    $adults   = (int) field('adults', 3);
    $children = (int) field('children', 3);
    $dateOk = function ($d) { $t = DateTime::createFromFormat('Y-m-d', $d); return $t && $t->format('Y-m-d') === $d; };

    if (!isset($PROPERTIES[$propKey]) || !$dateOk($checkin) || !$dateOk($checkout) || $checkout <= $checkin || $adults < 1) {
        respond(false, 'Please choose a property and valid check-in / check-out dates.', $isAjax);
    }
    $nights = (new DateTime($checkin))->diff(new DateTime($checkout))->days;
    $mailSubject = "Booking enquiry: {$PROPERTIES[$propKey]} ({$checkin} to {$checkout}) - {$name}";
    $lines = [
        'Property'  => $PROPERTIES[$propKey],
        'Check-in'  => $checkin,
        'Check-out' => $checkout . " ({$nights} night" . ($nights === 1 ? '' : 's') . ')',
        'Adults'    => $adults,
        'Children'  => max(0, $children),
    ];
} else {
    if ($message === '') {
        respond(false, 'Please write a message.', $isAjax);
    }
    $mailSubject = 'Website enquiry' . ($subject !== '' ? ": {$subject}" : '') . " - {$name}";
}

$body  = ($type === 'booking' ? "New booking enquiry" : "New contact message") . " from the TripTree website\n\n";
$body .= "Name: {$name}\nEmail: {$email}\nPhone: {$phone}\n";
if ($subject !== '') { $body .= "Subject: {$subject}\n"; }
foreach ($lines as $k => $v) { $body .= "{$k}: {$v}\n"; }
$body .= "\nMessage:\n" . ($message !== '' ? $message : '(none)') . "\n\n";
$body .= '---' . "\nSent: " . date('d M Y, H:i') . ' | IP: ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n";

$headers = [
    'From: ' . $SITE_NAME . ' <' . $FROM_EMAIL . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion(),
];

$sent = mail($TO_EMAIL, '=?UTF-8?B?' . base64_encode($mailSubject) . '?=', $body, implode("\r\n", $headers), '-f' . $FROM_EMAIL);

if ($sent) {
    $msg = $type === 'booking'
        ? 'Thank you! Your booking enquiry has been sent. We will contact you shortly to confirm availability.'
        : 'Thank you! Your message has been sent. We will get back to you shortly.';
    respond(true, $msg, $isAjax);
}
respond(false, 'Sorry, your message could not be sent. Please call us on +91 99000 05639 or email booking@triptree.co.in.', $isAjax);
