var Presentations = {
	copyPresentationURL : '/copy_presentation_content',
	getSlideContentURL: '/get_slide_content/',
	
	copySlideContent: function() {
		var windowSize = ["width=500, height=400, scrollbars=1"];
		var windowName = "Wybierz prezentację";
		
		
		newWindow = window.open(Presentations.copyPresentationURL, windowName, windowSize);
	},
	
	getSlideContent: function(slideId) {
		$.post(Presentations.getSlideContentURL + slideId 
		, {}
		, function(data) {
			if (data.success) {
				window.opener.Presentations.setSlideContent(data);
			}
		});
	},
	
	setSlideContent: function(slideData) {
		var newContent = slideData['content'];
		var newDescription = slideData['description'];
		
		tinyMCE.activeEditor.setContent(newContent);
		$('#description').val(newDescription);
	},
	
	presentationFileBrowser: function(field_name, url, type, win) {
		console.debug("Field_Name: " + field_name + "nURL: " + url + "nType: " + type + "nWin: " + win); // debug/testing
		var cmsURL = window.location.toString();    // script URL - use an absolute path!
		console.debug ('cms: '+cmsURL)
		cmsURL = cmsURL + "loadimages/";
		
		tinyMCE.activeEditor.windowManager.open({
	        file : cmsURL,
	        title : 'Menadżer obrazów',
	        width : 420,  // Your dimensions may differ - toy around with them!
	        height : 400,
	        resizable : "yes",
	        close_previous : "no"
	    }, {
	        window : win,
	        input : field_name
	    });
	    return false;



	}
}