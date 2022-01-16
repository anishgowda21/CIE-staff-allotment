function formateTime(time){
    time = time.split(':');
    (time[0] < 10) ? time[0] = "0"+time[0] : time[0] = time[0];
    time = time.join(':');
    return time;

}


function formateAMPM(time){
    time = time.split(':');
    var ampm = time[0] >= 12 ? 'PM' : 'AM';
    time[0] = time[0] % 12;
    time[0] = time[0] ? time[0] : 12;
    time.pop();
    time = time.join(':');
    return time + ' ' + ampm;
}

function enableButton()
{
    var selectelem = document.getElementById('sem-select-slt');
    var btnelem = document.getElementById('sem-slt-btn');
    btnelem.disabled = !selectelem.value;
}

$(document).on("click", ".time-del-btn",function(){
    var rec_id = $(this).data('id');
    console.log(rec_id);
    $("#deleteTimeModel").find(".modal-body #delTime-mod-id").val(rec_id);
  });

$(document).on("click", ".fac-del-btn",function(){
var rec_id = $(this).data('id');
console.log(rec_id);
$("#deleteFacModel").find(".modal-body #delFac-mod-id").val(rec_id);
});

$(document).on("click", ".time-edit-btn",function(){
var rec_id = $(this).data('id');
var code = $(this).data('cc');
var name = $(this).data('cn');
var date = $(this).data('ed');
var startTime = formateTime(($(this).data('est')));
var endTime = formateTime(($(this).data('eet')));
var ff = $(this).data('ff');
$("#updateTimeModel").find(".modal-body #updateTime-mod-id").val(rec_id);
$("#updateTimeModel").find(".modal-body #updateTime-mod-code").val(code);
$("#updateTimeModel").find(".modal-body #updateTime-mod-name").val(name);
$("#updateTimeModel").find(".modal-body #updateTime-mod-date").val(date);
$("#updateTimeModel").find(".modal-body #updateTime-mod-stime").val(startTime);
$("#updateTimeModel").find(".modal-body #updateTime-mod-etime").val(endTime);
$("#updateTimeModel").find(".modal-body #updateTime-mod-ff").val(ff);

});

$(document).on("click", ".fac-edit-btn",function(){
var rec_id = $(this).data('rec_id');
var fac_id = $(this).data('fac_id');
var name = $(this).data('name');
var email = $(this).data('email');
var phone = $(this).data('phone');
var fac_da = $(this).data('fac_da');

$("#facultyUpdateModal").find(".modal-body #updateFac-rec_id").val(rec_id);
$("#facultyUpdateModal").find(".modal-body #updateFac-fac_id").val(fac_id);
$("#facultyUpdateModal").find(".modal-body #updateFac-name").val(name);
$("#facultyUpdateModal").find(".modal-body #updateFac-email").val(email);
$("#facultyUpdateModal").find(".modal-body #updateFac-phone").val(phone);
$("#facultyUpdateModal").find(".modal-body #updateFac-da").val(fac_da);
});

$(document).on("click",".update-sem-btn",function(){
    var sem = $(this).data('sem');
    var no_cou = $(this).data('sub');
    var ava_room = $(this).data('ava');
    var rooms = $(this).data('rooms');

    $("#updateSemModel").find(".modal-body #updateSem-mod-semester").val(sem);
    $("#updateSemModel").find(".modal-body #updateSem-mod-sub").val(no_cou);
    $("#updateSemModel").find(".modal-body #updateSem-mod-avaRooms").val(ava_room);
    $("#updateSemModel").find(".modal-body #updateSem-mod-rooms").val(rooms);
    $("#updateSemModel").find(".modal-body #updateSem-mod-totalDuties").val(ava_room*no_cou);

    $("#updateSem-mod-sub").on("keyup",function(){
        console.log("keyup on 1");
        var sub = $("#updateSem-mod-sub").val();
        var ava = $("#updateSem-mod-avaRooms").val();
        $("#updateSemModel").find(".modal-body #updateSem-mod-totalDuties").val(sub*ava);
    });
    
    $("#updateSem-mod-avaRooms").on("keyup",function(){
        console.log("keyup on 2");
        var sub = $("#updateSem-mod-sub").val();
        var ava = $("#updateSem-mod-avaRooms").val();
        $("#updateSemModel").find(".modal-body #updateSem-mod-totalDuties").val(sub*ava);
    });

});

//Automaticly populate #updateSem-mod-totalDuties based on multiplication of values in #updateSem-mod-sub and #updateSem-mod-avaRooms



$.expr[":"].contains = $.expr.createPseudo(function(arg) {
return function( elem ) {
    return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
};
});

$(document).ready(function(){
    //search all columns in faculty table
    $('#fac_searchall').keyup(function(){
        var search = $(this).val();
        $('#faculty-table tbody tr').hide();

        //count total search result
        var len = $('#faculty-table tbody tr:not(.notfound) td:contains("'+search+'")').length;

        //show search result
        if(len > 0){
            $('#faculty-table tbody tr:not(.notfound) td:contains("'+search+'")').each(function(){
                $(this).closest('tr').show();
            });
        }else{
            $('#faculty-table tbody tr.notfound').show();
        }
    });
});
//Turn input filed border to red and show error message on invalid input on #updateSem-mod-avaRooms
function validateSemform(){
    console.log("called onsubmit");
    var rooms = $("#updateSem-mod-rooms").val();
    var avaRooms = $("#updateSem-mod-avaRooms").val();
    rooms = rooms.split(",").filter(n=>n);
    console.log(rooms);
    if(rooms.length != avaRooms){
        $("#updateSem-mod-rooms").css("border","2px solid red");
        $(".error-msg").css("display","block");
        return false;
}
}

  //Get time and date string from class table and
var data = document.getElementById("time-table");
if (data){
    data = data.rows;
    for(var i = 1; i < data.length; i++){
        var stime = data[i].cells[3].innerHTML;
        var etime = data[i].cells[4].innerHTML;
        var date = data[i].cells[2].innerHTML;
        var faculties = data[i].cells[5].innerHTML;
        date = date.split("-").reverse().join("-");
        stime = formateAMPM(formateTime(stime));
        etime = formateAMPM(formateTime(etime));
        faculties = faculties.replaceAll(',', '<br>');
        data[i].cells[3].innerHTML = stime;
        data[i].cells[4].innerHTML = etime;
        data[i].cells[2].innerHTML = date;
        data[i].cells[5].innerHTML = faculties;
    }
    

}

var sem_data = document.getElementById("sem-info-table");
if (sem_data){
    sem_data = sem_data.rows;
    for(var i = 1; i < sem_data.length; i++){
        rooms = sem_data[i].cells[3].innerHTML;
        rooms = rooms.replaceAll(',', '<br>');
        sem_data[i].cells[3].innerHTML = rooms;
    }
}

var allot_table = document.getElementById("allotment-table");
if (allot_table){
    var data = allot_table.rows;
    for(var i = 1; i < data.length; i++){
        var stime = data[i].cells[3].innerHTML;
        console.log(stime);
        var date = data[i].cells[2].innerHTML;
        date = date.split("-").reverse().join("-");
        stime = formateAMPM(formateTime(stime));
        data[i].cells[3].innerHTML = stime;
        data[i].cells[2].innerHTML = date;
    }
}


$(document).ready(function(){
    //search all columns in faculty table
    $('#allot_searchall').keyup(function(){
        var search = $(this).val();
        $('#allotment-table tbody tr').hide();

        //count total search result
        var len = $('#allotment-table tbody tr:not(.notfound) td:contains("'+search+'")').length;

        //show search result
        if(len > 0){
            $('#allotment-table tbody tr:not(.notfound) td:contains("'+search+'")').each(function(){
                $(this).closest('tr').show();
            });
        }else{
            $('#allotment-table tbody tr.notfound').show();
        }
    });
});

