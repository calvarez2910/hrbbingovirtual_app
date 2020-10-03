// $(document).ready(function () {


	$("#menuModal .nav-link").click(function(){
		
		console.log("se termino el clic");
			$('#menuModal').on('hidden.bs.modal', function () {
				console.log("se termino");
			// element which needs to be scrolled to
			// theId = $(this).attr("href");
			// console.log(theId);
			// check if the url is right
			// if (theId.includes("/")){
				// theId = theId.substring(1);
			// }
			// var element = document.querySelector(theId);

			// scroll to element
			// element.scrollIntoView();
		});
			$('#menuModal').modal('hide');	
		
	});

// })
