/**
 * Created by admin on 2016/8/28.
 */
$(function () {
    //������ʽ�仯
    $('.alert-form input').change(function () {
        if ($(this).is(':checked')) {
            pa = $(this).parent()
            pa.css('color', '#c1c1c1')
        } else {
            $(this).parent().css('color', '#555555')
        }
    })

    // ������ఴť
    $('.cd-read-more').click(function () {
        text = $(this).attr('data')
        $('.show-text').text(text)
    })

    //���������
    $(window).scroll(function () {
        if ($(document).scrollTop() > 230) {
            $('.uk-navbar').css({
                'background-color':'#fff',
                'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',

            },'slow')
            $('.uk-navbar-brand').css({
               'color':'#444'
            })
        }else{
             $('.uk-navbar').css({
                'background-color':'rgba(255, 255, 255, 0)',
                 'box-shadow':'none'
            })
            $('.uk-navbar-brand').css({
               'color':'rgba(255, 255, 255, 0)'
            })
        }

        if ($(document).scrollTop() >= $(document).height() - $(window).height()) {
        //    �ײ�

        }
    });

//    ��������
    $('.date-picker').change(function(){
        date = $(this).val()
        $('.div-date').each(function(i){
            if ($(this).text() == date){
                height = $(this).offset().top
                height = height -250
                $('body, html').stop().animate({scrollTop:height}, 600, 'swing')
                //$().scrollTop(height)
            }
        })
        //h = $('.div-date').first().offset()
        //alert(h.top)
    })
})