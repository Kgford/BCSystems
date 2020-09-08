  $(document).on('change', 'select#_desc', function () {
	  var url = $("#selectForm").attr("dropdown-url"); 
	  var description = $(this).val();
	  var category = $( "#_category option:selected" ).text();
	  var model = $( "#_model option:selected" ).text();
	  var location1 = $( "#_site option:selected" ).text();
	  var shelf = $( "#_shelf option:selected" ).text();
	  //alert(`description = ${description}`)
	  //alert(`category = ${category}`)
	  //alert(`model = ${model}`)
	  //alert(`location1 = ${location1}`)
	  //alert(`shelf = ${shelf}`)
	  $.ajax({
			url: "inventory/index",
			data:{description:description, category:category, model:model, location:location, shelf:shelf},		
            success : function(json) {
              console.log("post deletion successful");
            },

            error : function(xhr,errmsg,err) {
                // Show an error
               console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }			
		})

});
	
	

	
