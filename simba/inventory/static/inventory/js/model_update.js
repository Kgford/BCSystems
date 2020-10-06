function model_update(model_id) {
	// Initialize new request
	const request = new XMLHttpRequest();
	request.open('POST', '/loadmode');
	// Callback function for when request is completed
	request.onload = () =>{
		//const data = JSON.parse(request.responseText)
		var res = JSON.parse(request.responseText)
		var indata = JSON.stringify(res)
		var _equi = JSON.parse(indata)
		var sucess = JSON.stringify(_equi["success"])
		var active_item
		
		if (sucess) {
			var model_id = res.model_list[num].id
			var model_des = res.model_list[num].description
			var model_cat = res.model_list[num].category
			var model_band = res.model_list[num].band
			var model_model = res.model_list[num].model
			var model_vendor = res.model_list[num].vendor
			var model_comment = res.model_list[num].comment
			
			//load values
		    document.getElementById('_band').value = model_band;
			document.getElementById('_category').value = model_cat;
			document.getElementById('_desc').value = model_des;
			document.getElementById('_model').value = model_model;
			document.getElementById('_vendor').value = model_vendor;
			document.getElementById('_comments').value = model_comment;
			document.getElementById('_md').innerHTML = `Model# ${Model_model}`;
			document.getElementById('m_id').value = model_id;
					
			
			//make update and delete buttons appear
			document.getElementById('_update').style.visibility = 'visible';
			document.getElementById('_delete').style.visibility = 'visible';
					
		};
	};	
	// Add data to send with request
	const data = new FormData();
	var id = model_id
	data.append("model_id", id);
	// Send request
	request.send(data);
	return false;
	
};