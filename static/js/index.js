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
		var data = {
			csrfmiddlewaretoken: csrf()
		};
		if (this._a){
			this._a = false;
			data.address = address;
			$('#result_loc').html('<progress></progress>');
		} else {
			data.lat = this._lat;
			data.lng = this._lng;
		}
		if (this._r){
			this._r = false;
			data.radius = $('#radius').val();
			$('#result_addrs').html('<progress></progress>');
		}
		action = true;
		$.ajax({
			url: './get_loc',
			type: 'POST',
			dataType: 'json',
			data: data,
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
	aj: function(flag){
		clearTimeout(this._t_get_loc);
		this[`_${flag}`] = true;
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
