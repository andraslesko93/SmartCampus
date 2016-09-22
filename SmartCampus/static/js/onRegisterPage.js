document.getElementById('uploadButton').onchange = function () {
		  document.getElementById('uploadFile').placeholder=this.value;
};


document.getElementById('user_form').onchange = function () {
	
	var pw=document.getElementById('id_password');
	var confirmPw=document.getElementById('id_confirm_password');
	
	if(pw.value != confirmPw.value)
	{
		document.getElementById('id_confirm_password').setCustomValidity("The two passwords should match.");
	}
	else
	{
		document.getElementById('id_confirm_password').setCustomValidity('');

	}
	
	var acceptTerms = document.getElementById('id_accept_terms') ;
	if (acceptTerms.checked==false)
	{
		acceptTerms.setCustomValidity("You have to accept the terms of use before register to the application");
	}
	else
	{
		acceptTerms.setCustomValidity('');
	}
	
};
