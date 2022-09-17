let action = false;
let csrf = function(){
	var token = $('input[name="csrfmiddlewaretoken"]').val();
	var list = document.cookie.split(';');
	for (var i = 0, el; i < list.length; i++){
		el = list[i].trim();
		if (el.startsWith('csrftoken=')){
			token = el.split('=')[1].trim();
			break;
		}
	};
	return token;
};

let get_loc = {
	_lat: null,
	_lng: null,
	_clear: function(){
		this._lat = null;
		this._lng = null;
		$('#result_loc').html('');
		$('#result_addrs').html('');
	},
	_get_loc: function(){
		var address = $('#address').val();
		if (!address.length)
			return;
		$('#result_loc').html('<progress></progress>');
		$('#result_addrs').html('');
		action = true;
		$.ajax({
			url: './get_loc',
			type: 'POST',
			dataType: 'json',
			data: {
				csrfmiddlewaretoken: csrf(),
				address: $('#address').val()
			},
			success: (json) => {
				if (this._resend){
					this._resend = false;
					return this._get_loc();
				}
				action = false;
				if (json.fail){
					this._clear();
					return alert(json.fail);
				}
				$('#result_loc').html(`${json.lat} : ${json.lng}`);
				this._lat = json.lat;
				this._lng = json.lng;
				get_addrs();
			},
			error: () => {
				action = false;
				this._clear();
				alert('ERROR');
			}
		});
	},
	aj: function(){
		clearTimeout(this._t_get_loc);
		this._t_get_loc = setTimeout(() => {
			if (action){
				this._resend = true;
				return
			}
			this._get_loc();
		}, 300);
	},
};

let change_radius = function(){
	var radius = $('#radius').val();
	$('#radius_label').html(`${radius} km`);
};

let get_addrs = function(){
	if (action)
		return;
	if (get_loc._lat === null)
		return;
	$('#radius').attr('disabled', true);
	$('#result_addrs').html('<progress></progress>');
	action = true;
	$.ajax({
		url: './get_addrs',
		type: 'POST',
		dataType: 'json',
		data: {
			csrfmiddlewaretoken: csrf(),
			lat: get_loc._lat,
			lng: get_loc._lng,
			radius: $('#radius').val()
		},
		success: (json) => {
			action = false;
			$('#radius').removeAttr('disabled');
			if (json.fail){
				$('#result_addrs').html('');
				return alert(json.fail);
			}
			$('#result_addrs').html(json.addrs.join('<br>'));
		},
		error: () => {
			action = false;
			$('#radius').removeAttr('disabled');
			$('#result_addrs').html('');
			alert('ERROR');
		}
	});
};
