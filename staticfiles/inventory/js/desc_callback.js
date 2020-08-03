document.addEventListener('DOMContentLoaded', () => {
	//description
	_desc.onchange = function(event){
		var _desc = event.target.options[event.target.selectedIndex].dataset.val;
		var _select = event.target.options[event.target.selectedIndex].dataset.desc;
		var selector = document.getElementById('_model');
        var _model = selector[selector.selectedIndex].value;
		selector = document.getElementById('_status');
        var _status = selector[selector.selectedIndex].value;
		selector = document.getElementById('_category');
        var _cat = selector[selector.selectedIndex].value;
		selector = document.getElementById('_site');
        var _loc = selector[selector.selectedIndex].value;
		selector = document.getElementById('_shelf');
        var _shelf = selector[selector.selectedIndex].value;
				
		const request = new XMLHttpRequest();
		request.open('POST', '/searchinv');
		
		// Callback function for when request is completed
		request.onload = () =>{
			//const data = JSON.parse(request.responseText)
			var res = JSON.parse(request.responseText)
			var indata = JSON.stringify(res)
			var _equi = JSON.parse(indata)
			var sucess = JSON.stringify(_equi["success"])
			var active_inv
			
			//Clear table
			$('#table_id').empty()
			//Add header
			var table = document.getElementById('table_id')
			var row1 = table.insertRow(-1);
			var headerCell = document.createElement("TH");
			headerCell.innerHTML = 'Category'
			row1.appendChild(headerCell);
			headerCell = document.createElement("TH");
			headerCell.innerHTML = 'Status'
			row1.appendChild(headerCell);
			headerCell = document.createElement("TH");
			headerCell.innerHTML = 'Description'
			row1.appendChild(headerCell);
			headerCell = document.createElement("TH");
			headerCell.innerHTML = 'Model'
			row1.appendChild(headerCell);
			headerCell = document.createElement("TH");
			headerCell.innerHTML = 'S/N'
			row1.appendChild(headerCell);
			headerCell = document.createElement("TH");
			headerCell.innerHTML = 'Location'
			row1.appendChild(headerCell);
			headerCell = document.createElement("TH");
			headerCell.innerHTML = 'Quantity'
			row1.appendChild(headerCell);
			headerCell = document.createElement("TH");
			headerCell.innerHTML = 'Comments'
			row1.appendChild(headerCell);
			headerCell = document.createElement("TH");
			headerCell.innerHTML = 'Active'
			row1.appendChild(headerCell);
			
			//Add rows
			if (sucess) {
				// Load the entire inventory
				var num = 0;
				var a = "" ;
				for (active_inv in res.inv_list) { 
				var inv_cat = res.inv_list[num].category
				var inv_stat = res.inv_list[num].status
				var inv_desc = res.inv_list[num].description
				var inv_model = res.inv_list[num].model
				var inv_sn = res.inv_list[num].serial_number
				var inv_loc = res.inv_list[num].location
				var inv_quan = res.inv_list[num].quantity
				var inv_remarks = res.inv_list[num].remarks
				var inv_active = res.inv_list[num].active
				
				var tr = document.createElement("tr");
				var row=document.getElementById('table_id').insertRow()
				var cell1 = row.insertCell(0)
				var cell2 = row.insertCell(1)
				var cell3 = row.insertCell(2)
				var cell4 = row.insertCell(3)
				var cell5 = row.insertCell(4)
				var cell6 = row.insertCell(5)
				var cell7 = row.insertCell(6)
				var cell8 = row.insertCell(7)
				var cell9 = row.insertCell(8)
				var pathArray = window.location.href;
				pathArray = pathArray.substring(0, pathArray.lastIndexOf("/"));
				var url = `${pathArray}/item/${res.inv_list[num].id}`
				//alert(url)
				// Create the text node for anchor element. 
				cell1.innerHTML = `<a href=${url}>${inv_cat}</a>`;
				cell2.innerHTML = `<a href=${url}>${inv_stat}</a>`;
				cell3.innerHTML = `<a href=${url}>${inv_desc}</a>`;
				cell4.innerHTML = `<a href=${url}>${inv_model}</a>`;
				cell5.innerHTML = `<a href=${url}>${inv_sn}</a>`;
				cell6.innerHTML = `<a href=${url}>${inv_loc}</a>`;
				cell7.innerHTML = `<a href=${url}>${inv_quan}</a>`;
				cell8.innerHTML = `<a href=${url}>${inv_remarks}</a>`;
				cell9.innerHTML = `<a href=${url}>${inv_active}</a>`;
				num++;					
				};
			};
		};
		// Add data to send with request
		const data = new FormData();
		data.append("sel",_select);
		data.append("desc", _desc);
		data.append("model", _model);
		data.append("status", _status);
		data.append("category", _cat);
		data.append("location", _loc);
		data.append("shelf", _shelf);
		// Send request
		request.send(data);
		return false;
	};
	
});
	
	

	
