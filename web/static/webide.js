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

function savemode() {
    
    $.post(ajaxURL + "/save", { fpath: currentmode, contents: editor.getValue() })
    .done(function(data) {
         // alert(data);
    });
}

function sendReload() {
    
    $.post(ajaxURL + "/send_reload", {name: currentmode })
    .done(function(data) {
         // alert(data);
    });
}

function editorSetSyntax(syntax){
   if (syntax == "py") editor.getSession().setMode("ace/mode/python");
   if (syntax == "lua") editor.getSession().setMode("ace/mode/lua");
}

$(document).ready(function() {

 
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

    $("#reload-mode").click(function() {
        sendReload();
    });

    $("#save").click(function() {
        savemode();
    });

});
