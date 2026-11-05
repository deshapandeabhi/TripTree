/* TripTree contact & booking forms: validation + AJAX submit to inc/sendemail.php */
(function ($) {
    'use strict';

    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function isoDate(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }

    // Booking form: preselect property from ?property=slug and keep dates sensible
    var $booking = $('.booking-form');
    if ($booking.length) {
        var match = /[?&]property=([a-z0-9-]+)/.exec(window.location.search);
        var $prop = $('#b-property');
        if (match && $prop.find('option[value="' + match[1] + '"]').length) {
            $prop.val(match[1]);
            if ($.fn.niceSelect) { $prop.niceSelect('update'); }
        }
        var today = isoDate(new Date());
        var $in = $('#b-checkin'), $out = $('#b-checkout');
        $in.attr('min', today);
        $out.attr('min', today);
        $in.on('change', function () {
            if (!this.value) { return; }
            var next = new Date(this.value + 'T00:00:00');
            next.setDate(next.getDate() + 1);
            $out.attr('min', isoDate(next));
            if (!$out.val() || $out.val() <= this.value) { $out.val(isoDate(next)); }
        });
    }

    function validate($form) {
        var errors = [];
        $form.find('.is-invalid').removeClass('is-invalid');
        $form.find('input, select, textarea').each(function () {
            if (this.name === 'website' || this.type === 'hidden') { return; }
            if (!this.checkValidity()) {
                var $el = $(this);
                $el.addClass('is-invalid');
                $el.next('.nice-select').addClass('is-invalid');
                errors.push(this);
            }
        });
        var $in = $form.find('[name="checkin"]'), $out = $form.find('[name="checkout"]');
        if ($in.length && $in.val() && $out.val() && $out.val() <= $in.val()) {
            $out.addClass('is-invalid');
            errors.push($out[0]);
        }
        return errors;
    }

    $('.js-ajax-form').on('submit', function (e) {
        e.preventDefault();
        var $form = $(this);
        var $status = $form.find('.form-status');
        var $btn = $form.find('button[type="submit"]');

        var errors = validate($form);
        if (errors.length) {
            $status.removeClass('is-success').addClass('is-error')
                .text('Please fill in the highlighted fields correctly.');
            $(errors[0]).trigger('focus');
            return;
        }

        $btn.prop('disabled', true);
        $status.removeClass('is-error is-success').text('Sending...');

        fetch($form.attr('action'), {
            method: 'POST',
            body: new FormData(this),
            headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
        }).then(function (res) {
            return res.json().catch(function () { return { ok: false }; });
        }).then(function (data) {
            if (data && data.ok) {
                $status.addClass('is-success').text(data.message || 'Thank you! We will get back to you shortly.');
                $form[0].reset();
                if ($.fn.niceSelect) { $form.find('select').niceSelect('update'); }
            } else {
                throw new Error((data && data.message) || 'send failed');
            }
        }).catch(function (err) {
            var msg = (err && err.message && err.message !== 'send failed' && err.message.indexOf('fetch') === -1)
                ? err.message
                : 'Sorry, your message could not be sent. Please call us on +91 99000 05639 or email booking@triptree.co.in.';
            $status.addClass('is-error').text(msg);
        }).then(function () {
            $btn.prop('disabled', false);
        });
    });
})(jQuery);
