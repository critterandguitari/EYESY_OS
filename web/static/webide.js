editor = null
currentmode = ''
ajaxURL = 'http://' + location.host

function getFile(fpath) {

    $.get(ajaxURL + '/get_file/?fpath='+encodeURIComponent(fpath), function(data) {
        editor.setValue(data)
        editor.gotoLine(1)
        currentmode = fpath
        $("#title").html(fpath)
    });
}


function saveNewmode() {
    
    newName = prompt('Enter New Name (No Spaces!)')

    if (newName == null) {
        alert('f');
    }

    $.post(ajaxURL + "/save_new", { name: newName, contents: editor.getValue() })
    .done(function(data) {
        // reload mode list
         // alert(data);
    });
}

function savemode() {
    
    $.post(ajaxURL + "/save", { fpath: currentmode, contents: editor.getValue() })
    .done(function(data) {
         // alert(data);
    });
}

function sendReload() {
    
    //$.post(ajaxURL + "/send_reload", { name: currentmode, contents: editor.getValue() })
    $.post(ajaxURL + "/send_reload", {name: currentmode })
    .done(function(data) {
         // alert(data);
    });
}

$(document).ready(function() {

    // this disables page while loading things 
/*    $("body").on({
        // When ajaxStart is fired, add 'loading' to body class
        ajaxStart: function() { 
            $(this).addClass("loading");
            console.log("ajax start")
        },
        // When ajaxStop is fired, rmeove 'loading' from body class
        ajaxStop: function() { 
            $(this).removeClass("loading"); 
            console.log("ajax stop")
        }    
    });*/
 
    // this disables page while loading things 
    $(document).ajaxStart (function() { 
            $('body').addClass("loading");
            console.log("ajax start")
    });
        // When ajaxStop is fired, rmeove 'loading' from body class
    $(document).ajaxStop (function() { 
            $('body').removeClass("loading"); 
            console.log("ajax stop");        
    });
        
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/merbivore_soft");
    //editor.getSession().setMode("ace/mode/lua");
    editor.getSession().setMode("ace/mode/python");
    //$("#editor").style.fontSize='16px';
    document.getElementById('editor').style.fontSize='14px';

    $("#clear-screen").click(function() {
        sendCmd("cs\n");
    });

    $("#screengrab").click(function() {
        sendCmd("screengrab\n");
    });

    $("#reload-mode").click(function() {
        sendReload();
    });

    $("#osd-toggle").click(function() {
        sendCmd("osd\n");
    });

    $("#quit").click(function() {
        sendCmd("quit\n");
    });

    $("#save-new").click(function() {
        saveNewmode();
    });

    $("#save").click(function() {
        savemode();
    });

});
