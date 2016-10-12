var editor
var right_click
(function () {
    $(function () {
        var $preview, toolbar;
        Simditor.locale = 'zh-CN';
        toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough', 'fontScale', 'color', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'image', 'hr', '|', 'indent', 'outdent', 'alignment'];
        editor = new Simditor({
            textarea: $('#editor'),
            placeholder: 'enter here...',
            toolbar: toolbar,
            pasteImage: true,
            //{#                defaultImage: 'assets/images/image.png',#}
            upload: location.search === '?upload' ? {
                url: '/upload'
            } : false
        });
        $preview = $('#preview');
        if ($preview.length > 0) {
            return editor.on('valuechanged', function (e) {
                return $preview.html(editor.getValue());
            });
        }
    });

}).call(this);

$(function () {
    text = editor.getValue()
    $('.visual div').empty().append(text)

    editor.on('valuechanged', function (src, e) {
        text = editor.getValue()
        $('.visual div').empty().append(text)
        //{#            test = '<p><span style="color: rgb(32, 147, 97);">\'hello\', nihao "asdasd"</span><br>&nbsp;<br></p>'  //����취ת��#}
        //{#            $('.simditor-body').append(test)#}
        //{#            alert(text)#}
    })
    //
    $('.close').click(function () {
        $('.visual div').slideToggle()
        if ($(this).hasClass('uk-icon-chevron-up')) {
            $(this).removeClass('uk-icon-chevron-up')
            $(this).addClass('uk-icon-chevron-down')
            $('.visual').css('opacity', '0.2')
        } else if ($(this).hasClass('uk-icon-chevron-down')) {
            $(this).removeClass('uk-icon-chevron-down')
            $(this).addClass('uk-icon-chevron-up')
            $('.visual').css('opacity', '1')
        }
        //{#            $('.visual').css('opacity', '0.2')#}
    })

    //
    //{#        $(".left-side").mouseover(function () {#}
    //{#             $('.left-top').show()#}
    //{#            $(this).stop().animate({#}
    //{#                width: "310px"#}
    //{#            }).mouseout(function () {#}
    //{#                $('.left-top').hide()#}
    //{##}
    //{#                $(this).stop().animate({#}
    //{#                    width: "10px"#}
    //{#                });#}
    //{#            });#}
    //{#        });#}

    $('.menu').click(function () {

        div = $(this).siblings()
        li = $(this).parents('li')
        if (div.is(':hidden')) {
            li.addClass('uk-open')
        } else {
            li.removeClass('uk-open')
        }
        div.slideToggle()
    })


    $('.left-content').bind('contextmenu', function (e) {
        return false
    })
    $('.uk-nav-sub li').mousedown(function (e) {
        if (e.which == 3) {
            x = e.pageX
            y = e.pageY - 150
            lis = '<li class="pm"><i class="uk-icon-clone"></i> copy</li>' +
                '<li class="pm"><i class="uk-icon-paste"></i> paste</li> ' +
                '<li class="pm del-doc"><i class="uk-icon-eraser"></i> del</li> ' +
                '<li class="pm"><i class="uk-icon-cut"></i> cut</li> ' +
                '<li class="pm rename"><i class="uk-icon-edit"></i> rename</li>'
            $('.mouse-menu .uk-list').empty().append(lis)
            right_click = $(this)
            $('.mouse-menu').css({
                top: y,
                left: x,
                display: 'block',
            })
        } else {
            $('.mouse-menu').hide()
        }
    })
    $('.menu').mousedown(function (e) {
        if (e.which == 3) {
            x = e.pageX
            y = e.pageY - 150
            lis = '<li class="pm new-doc"><i class="uk-icon-file-o "></i> new-doc</li>'
                + '<li class="pm new-type" id="ne"><i class="uk-icon-plus "></i> new-type</li>'
                + '<li class="pm del-type"><i class="uk-icon-remove "></i> del-type</li>'
            $('.mouse-menu .uk-list').empty().append(lis)
            right_click = $(this)
            $('.mouse-menu').css({
                top: y,
                left: x,
                display: 'block',
            })

        } else {
            $('.mouse-menu').hide()
        }
    })
    $('body').mousedown(function (e) {
        obj = $(e.target)
        if (!obj.hasClass('pm')) {
            if (e.which != 3) {
                $('.mouse-menu').hide()
            }
        }
    })

    //    --------------------右键菜单事件----------------------
    $('body').on('click', '.new-doc', function (event) {
        event.stopPropagation();
        $p = right_click
        type = $p.attr('data')
        if (type == null) {
            return false
        }
        UIkit.modal.prompt("Create a new document", '', function (value) {
            $.ajax({
                type: 'post',
                url: '/add/note',
                data: {
                    'type': type,
                    'value': value,
                },
                success: function (msg) {
                    if (msg.msg != 'ok') {
                        alert('无法新建文档，请检查网络是否断开...')
                    } else {
                        $p.siblings().children().append(' <li class="notes" data="' + msg.id + '"><a ><i class="uk-icon-file-text-o"></i> ' + value + '</a></li>')
                    }
                }
            })
        });
    })
    $('body').on('click', '.del-doc', function (event) {
        event.stopPropagation();
        $p = right_click
        id = $p.attr('data')
        UIkit.modal.confirm('The doc will be del, are you sure to do this?', function () {
            $.ajax({
                type: 'post',
                url: '/del/note',
                data: {
                    'id': id,
                },
                success: function (msg) {
                    if (msg.msg != 'ok') {
                        alert('can not del the doc, check the network...')
                    } else {
                        $('.mouse-menu').hide()
                        $p.hide()
                        alert('del the doc successfully')
                    }
                }
            })
        })

    })

    $('body').on('click', '.new-type', function (event) {
        UIkit.modal.prompt("Create a new type", '', function (value) {
            if (value == '') {
                alert('can not blank')
                return false
            }
            $.ajax({
                type: 'post',
                url: '/add/note',
                data: {
                    'new-type': value,
                },
                success: function (msg) {
                    if (msg.msg != 'ok') {
                        alert('无法新建文档，请检查网络是否断开...')
                    } else {
                        window.location.reload()
                    }
                }
            })
        });
    })

    $('body').on('click', '.rename', function (event) {
        $p = right_click
        id = $p.attr('data')
        UIkit.modal.prompt("enter a new name", $p.find('span').text(), function (value) {
            if (value == '') {
                alert('can not blank')
                return false
            }
            $.ajax({
                type: 'post',
                url: '/save/note',
                data: {
                    'new-name': value,
                    'id': id
                },
                success: function (msg) {
                    if (msg.msg != 'ok') {
                        alert('can not rename the doc, check the network...')
                    } else {
                        $('.mouse-menu').hide()
                        $p.find('span').text(value)
                    }
                }
            })
        });
    })


    // 双击打开文档
    $(document).on('click', '.notes', function () {
        id = $(this).attr('data')
        $('.save').attr('data', id)
        $.ajax({
            type: 'post',
            url: '/get/note',
            data: {
                'id': id
            },
            success: function (res) {
                $('.information').text(res.note.type + ' > ' + res.note.title)
                $('.p-desc').val(res.note.desc)
                editor.setValue(res.note.content)
                if (res.note.show) {
                    $('.p-hide').addClass('uk-icon-eye').removeClass('uk-icon-eye-slash')
                } else {
                    $('.p-hide').removeClass('uk-icon-eye').addClass('uk-icon-eye-slash')
                }
            }
        })
    })

//  保存文档 ajax
    $('.save').click(function () {
        save_notes()
    })
    $('.simditor-body').keyup(function(){
        save_notes()
    })
    function save_notes(){
        id = $('.save').attr('data')
        if (id == '') {
            alert('can not find the doc')
            return false
        }
        $.ajax({
            url: '/save/note',
            type: 'post',
            data: {
                'id': id,
                'value': editor.getValue(),
                'desc': $('.p-desc').val()
            },
            success: function (msg) {
                if (msg.msg != 'ok') {
                    alert('can not save the document, check the network...')
                } else {
                    //alert('save success')
                    $('.info').show()
                    setTimeout(function(){
                        $('.info').hide()
                    }, 2500)
                }
            }
        })
    }

//    隐藏切换
    $('.p-hide').click(function () {
        var bol
        id = $('.save').attr('data')
        if (id == '') {
            alert('can not find the doc')
            return false
        }
        if ($(this).hasClass('uk-icon-eye')) {
            $(this).removeClass('uk-icon-eye').addClass('uk-icon-eye-slash')
            bol = false
        } else {
            $(this).addClass('uk-icon-eye').removeClass('uk-icon-eye-slash')
            bol = true
        }

        $.ajax({
            url: '/save/note',
            type: 'get',
            data: {
                'id': id,
                'bol': bol,
            },
            success: function (msg) {
                if (msg.msg != 'ok') {
                    alert('can not toggle show/hide, check the network...')
                } else {
                    alert('toggle successfully')
                }
            }
        })

    })
})
