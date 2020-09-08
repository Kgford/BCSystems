function event_load(event_id) {
	// Initialize new request
	const request = new XMLHttpRequest();
	request.open('POST', '/loadevent');
	// Callback function for when request is completed
	request.onload = () =>{
		//const data = JSON.parse(request.responseText)
		var res = JSON.parse(request.responseText)
		var indata = JSON.stringify(res)
		var _equi = JSON.parse(indata)
		var sucess = JSON.stringify(_equi["success"])
		var active_item
		
		if (sucess) {
			var event_type = res.event_list[0].event_type
			var event_comment = res.event_list[0].comment
			var event_date = res.event_list[0].event_date
			var event_loc = res.event_list[0].location
			var event_rma = res.event_list[0].rma
			var event_mr = res.event_list[0].mr
			
			//load values
		    document.getElementById('_event').value = event_type;
			document.getElementById('_loc').value = event_loc;
			document.getElementById('_date').value = event_date;
			document.getElementById('_rma').value = event_rma;
			document.getElementById('_mr').value = event_mr;
			document.getElementById('_comments').value = event_comment;
			document.getElementById('_event_change').innerHTML = `Update Event# ${event_id}`;
			document.getElementById('e_id').value = event_id;
		
			
			//make update and delete buttons appear
			document.getElementById('_update').style.visibility = 'visible';
			document.getElementById('_delete').style.visibility = 'visible';
			document.getElementById('e_id').style.visibility = 'visible';
			document.getElementById('el_id').style.visibility = 'visible';
			document.getElementById('_save').style.visibility = 'hidden';
		
		};
	};	
	// Add data to send with request
	const data = new FormData();
	var id = event_id
	data.append("event_id", id);
	// Send request
	request.send(data);
	return false;
	
};