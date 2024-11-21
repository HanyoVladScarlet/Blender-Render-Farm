// Refer to: https://stackoverflow.com/questions/10899384/uploading-both-data-and-files-in-one-form-using-ajax
$('#blender-file-uploader').submit(function(e){
    e.preventDefault();
    var formData = new FormData(this);
    // TODO: Use ajax to create task here.
    // Use ajax to upload files.
    $.ajax({
        'url': '/api/upload/with-bpy',
        'type': 'POST',
        'success': function(data){
            console.log(data)
        },
        'data': formData,
        'cache': false,
        'processData': false,
        'contentType': false       
    });
    
});
setInterval(function(){
    try {
        $.ajax({
            'url': '/api/get-info',
            'type': 'GET',
            'success': function(data) {
                $('#info').text(data)
            },
            'error': function(e) {},
            'cache': false,
            'processData': false,
            'contentType': false       
            });
    }
    catch (e) {}
}, 1000);