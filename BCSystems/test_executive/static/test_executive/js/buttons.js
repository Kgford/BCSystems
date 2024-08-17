$(document).ready(function () {
    //onchange of rooms-count

    $(document).on('change', '#rooms', function () {

        var roomsSelected = $('#rooms option:selected').val();
        var roomsDisplayed = $('[id^="room-"]:visible').length;
        var roomsRendered = $('[id^="room-"]').length;
        var orig = $('#peoplerooms').find(roomsSelected);

        //if room count is greater than number displayed - add or show accordingly
        if (roomsSelected > roomsDisplayed) {

            for (var i = 1; i <= roomsSelected; i++) {
                var r = $('#room-' + i);
                if (r.length == 0) {

                    var clone = $('#room-1').clone(); //clone
                    clone.children(':first').text("Room " + i);
                    //change ids appropriately
                    setNewID(clone, i);
                    clone.children('div').children('select').each(function () {
                        setNewID($(this), i);
                    });
                    $(clone).insertAfter($('#room-' + roomsRendered));

                } else {
                    //if the room exists and is hidden 
                    $(r).show();
                }
            }

        } else {
            //else if less than room count selected - hide
            for (var i = ++roomsSelected; i <= roomsRendered; i++) {
                $('#room-' + i).hide();
            }
        }

    });

    function setNewID(elem, i) {
        oldID = elem.attr('id');
        newId = oldID.substring(0, oldID.indexOf('-')) + "-" + i;
        elem.attr('id', newId);
    }

});







// TOP CONTROLS
$('.plus').click(function (e) {
        e.preventDefault();
    var sp = parseFloat($(this).prev('span').text());
    $(this).prev('span').text(sp + 1);
});

$('.minus').click(function (e) {
        e.preventDefault();
    var sp = parseFloat($(this).next('span').text());
    $(this).next('span').text(sp - 1);
    if (!isNaN(sp) && sp > 0) {
        $(this).next('span').text(sp - 1);
    } else {
        $(this).next('span').text(0);
    }
});



//POPOVER CONTROLS


var isVisible = false;
var clickedAway = false;

$('#travelpeople').popover({
    html: true,
    trigger: 'manual',
    content: function () {
        return $('#peoplerooms').html();
    }
}).click(function (e) {
    $(this).popover('show');
    clickedAway = false
    isVisible = true
    e.preventDefault()
    $('.popover').bind('click', function () {
        clickedAway = false
        //alert('popover has been clicked!');
    });
});

$(document).click(function (e) {
    if (isVisible && clickedAway) {
        $('#travelpeople').popover('hide');
        isVisible = clickedAway = false
    } else {
        clickedAway = true
    }
});

    
$('body').on('click touchstart', 'button.qtyplus', function () {

var btn = $('.popover').find('.qtyplus');
var qtyCurrent = $('.popover').find('.qty');
var qtyValue = parseInt($('.popover').find('.qty').val());
var currentVal = parseInt(qtyValue);
    if (!isNaN(currentVal)) {
        $(qtyCurrent).val(currentVal + 1);
    } else {
        $(qtyCurrent).val(0);
    }
          e.preventDefault();
});
// This button will decrement the value till 0
$(".qtyminus").click(function (e) {

    e.preventDefault();
    fieldName = $(this).attr('field');

    var currentVal = parseInt($('input[name=' + fieldName + ']').val());

    if (!isNaN(currentVal) && currentVal > 0) {
        $('input[name=' + fieldName + ']').val(currentVal - 1);
    } else {
        $('input[name=' + fieldName + ']').val(0);
    }
});