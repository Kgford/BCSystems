 // Delete post on click
$("#talk").on('click', 'a[id^=delete-post-]', function(){
    var post_primary_key = $(this).attr('id').split('-')[2];
    alert(post_primary_key) // sanity check
    update desc(post_primary_key);
});
 
 
 
 
 
 
 
 
 function update desc(post_primary_key){
   $.ajax({
		url : "searchall/", // the endpoint
		type : "POST", // http method
		data : { postpk : post_primary_key }, // data sent with the delete request
		success : function(json) {
			// hide the post
		  $('#post-'+post_primary_key).hide(); // hide the post on success
		  console.log("post deletion successful");
		},

		error : function(xhr,errmsg,err) {
			// Show an error
			$('#results').html("<div class='alert-box alert radius' data-alert>"+
			"Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
};