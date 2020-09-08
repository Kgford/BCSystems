 window.addEventListener('load', function(event) {
	function ajaxFunction(argId){
	 var ajaxRequest;  // The variable that makes Ajax possible!
	 try{
		// Opera 8.0+, Firefox, Safari
		ajaxRequest = new XMLHttpRequest();
	 }catch (e){
	   // Internet Explorer Browsers
	   try{
		  ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
	   }catch (e) {
		  try{
			 ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
		  }catch (e){
			 // Something went wrong
			 alert("Your browser broke!");
			 return false;
		  }
	   }
	 }
		// Create a function that will receive data 
		// sent from the server and will update
		// div section in the same page.
		ajaxRequest.onreadystatechange = () =>{
			//const data = JSON.parse(request.responseText)
			var res = JSON.parse(request.responseText)
			var indata = JSON.stringify(res)
			var _equi = JSON.parse(indata)
			var sucess = JSON.stringify(_equi["success"])
			var active_inv
			alert(res)
			
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
		// Now get the value from user and pass it to
		// server script.

		var queryString = "?q=" + argId ;
		ajaxRequest.open("GET", "getInputs.php" + 
								  queryString, true);
		ajaxRequest.send(null); 
		}
});		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	function load_items() {
		// Callback function for when request is completed
		request.onload = () =>{
			//const data = JSON.parse(request.responseText)
			var res = JSON.parse(request.responseText)
			var indata = JSON.stringify(res)
			var _equi = JSON.parse(indata)
			var sucess = JSON.stringify(_equi["success"])
			var active_inv
			alert(res)
			
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
	};