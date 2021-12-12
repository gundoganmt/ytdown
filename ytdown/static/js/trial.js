$(function () {
    'use strict'

    $("#video-form").submit(function (e) {
        e.preventDefault();

        $('.btn-form').prop("disabled",true);
        $('.progress-container').removeClass('d-none');
        clear_download_box();
        progress();
        process();
    });

    function clear_download_box(){
      var tb_v = $('#tbody_video').children();
      var tb_w_s = $('#tbody_vid_w_s').children();
      var tb_a = $('#tbody_audio').children();

      for (var i = 1; i < tb_v.length; i++){
          tb_v[i].remove();
      }
      for (var i = 1; i < tb_w_s.length; i++){
          tb_w_s[i].remove();
      }
      for (var i = 1; i < tb_a.length; i++){
          tb_a[i].remove();
      }
      $('#vid_w_s_item').addClass('d-none');
      $('#audio_items').addClass('d-none');
    }

    // Progress bar
    var interval,
        progress = function(){
        var progressBar = $(".progress-bar");
        progressBar.css( "width", 0 + '%' ) ;
        var width = 0;
        interval = setInterval(frame, 400);
        function frame() {
            if (width >= 99) {
                clearInterval(id);
            } else {
                width++;
                progressBar.css( "width", width + '%' ) ;
            }
        }
    }

    function stopProgress(){
        $(".progress-bar").css( "width", 0 + '%' ) ;
        clearInterval(interval);
    }

    var process = function(){
        $(".alert").addClass("d-none");

        const xhr = new XMLHttpRequest();
        var form_data = new FormData();

        var csrf_token = $('#csrf_token').val();
        var inputValue = $(".video-link").val();
        var url = '/extractor';

        form_data.append("inputValue", inputValue);

        xhr.open('POST', url)
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
        xhr.onload = () =>{
          if(xhr.status == 200){
            $('.progress-container').addClass('d-none');
            $('.alert').removeClass('d-block');
            stopProgress();

            const result = JSON.parse(xhr.responseText);
            if(!result.error){
              $('.download-box').removeClass('d-none');

              $('img').attr('src', result.thumbnail);
              $('.title').text(result.title);
              $('#duration').text(result.duration);

              var videos = result.video_streams;
              for(var i = 0; i < videos.length; i++){
                $('#tbody_video').append('<tr>' +
                   '<td class="align-middle py-4">' +
                      '<span class="d-block">' +
                      videos[i].resolution + '(.' + videos[i].ext + ')' +
                      (videos[i].resolution == '1080p' || videos[i].resolution == '720p' ? '<span class="badge bg-gradient-danger">HD</span>': '') +
                      '</span>' +
                   '</td>' +
                   '<td class="align-middle">' +
                      '<span class="d-block">' + videos[i].filesize + '</span>' +
                   '</td>' +
                   '<td class="align-middle">' +
                      '<a class="btn mb-0" href="' + videos[i].video_url + '" title="Download">' +
                      '<span class="d-block"><i class="fas fa-download fa-fw"></i> Download</span>' +
                      '</a>' +
                   '</td>' +
                '</tr>');
              }

              if ('video_without_sound' in result &&  result.video_without_sound.length > 0){
                var vid_w_s = result.video_without_sound;
                $('#vid_w_s_item').removeClass('d-none');
                for(var i = 0; i < vid_w_s.length; i++){
                  $('#tbody_vid_w_s').append('<tr>' +
                     '<td class="align-middle py-4">' +
                        '<span class="d-block">' +
                        vid_w_s[i].resolution + '(.' + vid_w_s[i].ext + ')' +
                        (vid_w_s[i].resolution == '1080p' || vid_w_s[i].resolution == '720p' ? '<span class="badge bg-gradient-danger">HD</span>': '') +
                        '</span>' +
                     '</td>' +
                     '<td class="align-middle">' +
                        '<span class="d-block">' + vid_w_s[i].filesize + '</span>' +
                     '</td>' +
                     '<td class="align-middle">' +
                        '<a class="btn mb-0" href="' + vid_w_s[i].video_url + '" title="Download">' +
                        '<span class="d-block"><i class="fas fa-download fa-fw"></i> Download</span>' +
                        '</a>' +
                     '</td>' +
                  '</tr>');
                }
              }

              if ('audio_streams' in result &&  result.audio_streams.length > 0){
                var audio = result.audio_streams;
                $('#audio_items').removeClass('d-none');
                for(var i = 0; i < audio.length; i++){
                  $('#tbody_audio').append('<tr>' +
                     '<td class="align-middle py-4">' +
                        '<span class="d-block">' +
                        audio[i].resolution + '(.' + audio[i].ext + ')' +
                        '</span>' +
                     '</td>' +
                     '<td class="align-middle">' +
                        '<span class="d-block">' + audio[i].filesize + '</span>' +
                     '</td>' +
                     '<td class="align-middle">' +
                        '<a class="btn mb-0" href="' + audio[i].video_url + '" title="Download">' +
                        '<span class="d-block"><i class="fas fa-download fa-fw"></i> Download</span>' +
                        '</a>' +
                     '</td>' +
                  '</tr>');
                }
              }

              $('.btn-form').prop("disabled",false);
              var $scollTo = $("#video-form");
              $([document.documentElement, document.body]).animate({
                  scrollTop: $scollTo.offset().top -20
              }, 750);
            }
            else{
              console.log('error')
              $('.alert').addClass('d-block');
            }
          }
          else {
            stopProgress();
            $('.progress-container').addClass('d-none');
            $('.alert').addClass('d-block');
          }
        }
        xhr.send(form_data);
        return false;
      }

    $('#submit').click(function(){
        $(this).addClass('d-none');
        $('.btn-spinner').addClass('d-inline-block');
    });


    /* Sidebar */
    $('.toggle-button ').click(function() {
        $('body').addClass('sidebar-toggled');
        $('.prevent-click').fadeIn();
    });


    $('body .prevent-click').click(function() {
        $('body').removeClass('sidebar-toggled');
        $('.prevent-click').fadeOut();
    });

    $('.question').on('click', function(){
        if( $(this).hasClass('active')){
            $(this).removeClass('active');
        }else{
            $(this).toggleClass('active');
        }
    });

    // Scroll to top button appear
    $(document).on('scroll', function() {
        var scrollDistance = $(this).scrollTop();
        if (scrollDistance > 100) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });


    // Smooth scrolling using jQuery easing
    $('a.scroll-to-top').on('click', function(e) {
        var $anchor = $(this);
        window.scrollTo({ top: 0, behavior: 'smooth' });
        e.preventDefault();
    });

});
