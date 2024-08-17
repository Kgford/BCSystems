window.onload = function()  {
  alert('we are here')
  const json = document.getElementById("list").value;
  alert(json)
  const item_list = JSON.parse(json);
  const inv_list = jQuery.parseJSON(item_list);
  for (i = 0; i < inv_list.length; i++) {
		 var str = '<TR height="20" ><TD class="HDR"> Category:{{active_inv.modelname}} </TD></TR>\
                 <TR height="20" ><TD NOWRAP="" class="STR0"> Model:  </TD><TD NOWRAP="" class="STR0"> inv_list[i].modelname</TD></TR>\
                 <TR height="10" ></TR>\
                 <TR height="20" ><TD NOWRAP="" class="STR0"> Total Quantity: </TD><TD NOWRAP="" class="STR0"> inv_list[i].total_quan </TD>\
				 <TD NOWRAP="" class="STR0">&nbsp In-Field Quantity: </TD><TD NOWRAP="" class="STR0"> inv_list[i].field_quan </TD>\
				 <TD NOWRAP="" class="STR0">&nbsp On-Site Quantity: </TD><TD NOWRAP="" class="STR0"> inv_list[i].site_quan </TD>\
				 <TD NOWRAP="" class="STR0">&nbsp In-Repair Quantity: </TD><TD NOWRAP="" class="STR0"> inv_list[i].In-Repair</TD>\
                 </tr>';
		$('#model_table').append(str);
	}