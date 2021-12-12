$(function () {
    'use strict'

    $("#video-form").submit(function (e) {
        e.preventDefault();

        $('.btn-form').prop("disabled",true);;
        $('.progress-container').removeClass('d-none');
        progress();
        process();
    });

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
            console.log(result);
            if(!result.error){
              $('.download-box').removeClass('d-none');
              var videos = result.video_streams;
              var tbody_video = document.getElementById('tbody_video');
              console.log(videos);
              for(var i = 0; i < videos.length; i++){
                console.log(tbody_video);
                console.log(videos[i].resolution);
                tbody_video.innerHtml += '<tr>' +
                   '<td class="align-middle py-4">' +
                      '<span class="d-block">' +
                      videos[i].resolution +
                      '<span class="badge bg-gradient-danger">HD</span>' +
                      '</span>' +
                   '</td>' +
                   '<td class="align-middle">' +
                      '<span class="d-block">' + videos[i].filesize + '</span>' +
                   '</td>' +
                   '<td class="align-middle">' +
                      '<a class="btn mb-0" href="' + videos[i].video_url + '" title="Download" style="background-color: #123c55;">' +
                      '<span class="d-block"><i class="fas fa-download fa-fw"></i> Download</span>' +
                      '</a>' +
                   '</td>' +
                '</tr>';
              }

              var $scollTo = $(".download-box");
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
