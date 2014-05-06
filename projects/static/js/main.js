var project = {};

project.countdown = {};

project.countdown.get = function (future) {

	var current = new Date().getTime(),
		originalDelta = (future - current) / 1000,
		data = {},
		delta;

	// Always work with a positive number, negate later if the original delta is negative
	delta = Math.abs(originalDelta);

	// Calculate (and subtract) whole days
	data.days = Math.floor(delta / 86400);
	delta -= data.days * 86400;

	// Negate the number of days if the original delta was negative
	if (originalDelta < 0) {
		data.days = 'Overdue by ' + Math.abs(data.days);
	}	

	// Calculate (and subtract) whole hours
	data.hours = Math.floor(delta / 3600) % 24;
	delta -= data.hours * 3600;

	// Calculate (and subtract) whole minutes
	data.minutes = Math.floor(delta / 60) % 60;
	delta -= data.minutes * 60;

	// The remainder is the number of seconds
	data.seconds = Math.floor(delta) % 60;

	return {
		timings: data,
		delta: originalDelta
	};
};

project.countdown.update = function ($field, data) {

	var $separator = '<span class="separator">,</span>',
		$currentUnit,
		cssClass,
		i = 0,
		prop;

	this.addStyleClass = function ($field, data) {

		var styleClass;
		
		// Manage CSS classes dependant on time remaining
		if (data.delta < 0) {
			styleClass = 'deploy-overdue';
		} else if (data.timings.days < 7) {
			styleClass = 'deploy-very-soon';
		} else if (data.timings.days >= 7 && data.timings.days < 14) {
			styleClass = 'deploy-soon';
		} else {
			styleClass = 'deploy-later';
		}

		// Add the correct class to the element
		$field.parent('li').removeClass('deploy-overdue deploy-very-soon deploy-soon deploy-later').addClass(styleClass);
	};

	// Loop over the time properties and update their respective containers
	for (prop in data.timings) {
		if (data.timings.hasOwnProperty(prop)) {

			$currentUnit = $field.find('.' + prop);
			
			if ($currentUnit.length > 0) {

				$currentUnit.html(data.timings[prop] + ' ' + (data.timings[prop] === 1 ? prop.replace(/s$/, '') : prop));

				// Add the comma separator to all but the last time property
				if (i < (Object.keys(data.timings).length - 1)) {
					$currentUnit.append($separator)
				}

				// Hide zero values from display
				if (prop !== 'seconds' && data.timings[prop] === 0) {
					$currentUnit.hide();
				} else {
					$currentUnit.show();
				}
			}
		}
		i++;
	}

	this.addStyleClass($field, data);
};

$(function() {

	var $fields = $('.open-project').find('.countdown'),
		future,
		data,
		iso,
		i;

	// Work out the remaining time every second
	window.setInterval(function () {

		for (i = 0; i < $fields.length; i++) {

			$this = $($fields[i]);

			// Get the date/time
			iso = $this.attr('data-timestamp');
			future = new Date(iso).getTime();
			
			// Calculate how much time is remaining for the current row
			data = project.countdown.get(future);

			// Update the page visually with the calculations
			project.countdown.update($this, data);
		}

	}, 1000);

	// By default Django adds an 'Unknown' value to the NullBooleanSelect select widget - remove this
	$('#id_is_complete').find('option:first').remove();

	// Step through the pagination every 10 seconds
	if ($('.pagination').length > 0) {
		window.setTimeout(function () {
			$current = $('.pagination').find('.current');
			$next = $current.next();

			if ($next.hasClass('disabled')) {
				$next = $('.pagination').find('.first');
			}

			window.location = $next.find('a').attr('href');
		}, 10000);
	}

});