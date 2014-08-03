jQuery(document).ready(function($){
 
	loadJS = function(src) {
		if (src.length == 0) return;
    	var jsLink = $("<script type='text/javascript' src='/assets/appjs/"+src+"'>");
     	$("#footer-scripts").append(jsLink); 
 	}; 
 	var $script_names = $('#script_name').html();

 	var $scripts = $script_names.split(',')
 	for(var $i = 0; $i < $scripts.length; $i++)
		loadJS($.trim($scripts[$i]));
});
