var project = {};

project.countdown = {};
project.constants = {};

project.countdown.get = function (current, future) {

	var data = null,
		delta;

	if (future - current > 0) {

		data = {};

		// get total seconds between the times
		delta = Math.abs(future - current) / 1000;

		// calculate (and subtract) whole days
		data.days = Math.floor(delta / 86400);
		delta -= data.days * 86400;

		// calculate (and subtract) whole hours
		data.hours = Math.floor(delta / 3600) % 24;
		delta -= data.hours * 3600;

		// calculate (and subtract) whole minutes
		data.minutes = Math.floor(delta / 60) % 60;
		delta -= data.minutes * 60;

		// what's left is seconds
		data.seconds = Math.floor(delta) % 60;

	}

	return data;
};

project.countdown.update = function ($field, data) {

	var prop;

	function manageStatusClass($field, add, remove) {
		$field.parent('li').removeClass(remove).addClass(add);
	}

	if (data !== null) {

		for (prop in data) {
			if (data.hasOwnProperty(prop)) {
				$field.find('.' + prop).html(data[prop])
			}
		}

		// Manage CSS classes dependant on time remaining
		if (data.days < 7) {
			manageStatusClass($field, 'deploy-very-soon', 'deploy-soon deploy-later');
		} else if (data.days >= 7 && data.days < 14) {
			manageStatusClass($field, 'deploy-soon', 'deploy-later');
		} else {
			manageStatusClass($field, 'deploy-later');
		}

	} else {
		$field.html('<span class="deploying">Deploying Now</span>');
		$field.parent('li').addClass('deploy-now');
	}

	$field.removeClass('invisible');
};

$(function() {

	var $fields = $('.open-project').find('.countdown'),
		current,
		future,
		data,
		iso,
		i;

	window.setInterval(function () {
		
		current = new Date().getTime();

		for (i = 0; i < $fields.length; i++) {
			$this = $($fields[i]);
			iso = $this.attr('data-timestamp');
			future = new Date(iso).getTime();
			data = project.countdown.get(current, future);
			project.countdown.update($this, data);
		}
	}, 1000);

});