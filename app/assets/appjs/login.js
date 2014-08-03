jQuery(document).ready(function($){
	console.log('From login.js');


	var signin = $("#loginbox")
	var registration = $("#signupbox")

	$(signin).on('click', '#btn-login', function(e) {
		e.stopPropagation();
		console.log('logging in');
		var username = $('#username').val();
		var password = $('#password').val();
		var rememberme = $('#login-remember:checked').val();
		rememberme = (rememberme === 1)? true: false;
		loginUser({
			username: username, 
			password:password, 
			remember:rememberme
		});
		return false;
	});

	var loginUser = function(options) {
		var uname = options.username;
		var passwd = options.password;
		var remember = options.remember;
		$.ajax({
    		type: 'POST',
    		url: '/login',
    		data: JSON.stringify({email: uname, password: passwd}),
    		success: function(data) { 
    			var message = data.message;
    			var node = data.node;
    			var status = data.status;
    			if (status == 'success') {
    				window.location.href = '/';
				}
				else {
					$('.alert').append(message);
					$('.alert').addClass('error');
					$('.alert').show();

				}
    		},
    		contentType: "application/json",
    		dataType: 'json'
		});
	};

});
