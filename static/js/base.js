$('.logout').click(function () {
        $.ajax({
            type:'post',
            url:'/logout/',
            data:'csrfmiddlewaretoken='+$('input[name="csrfmiddlewaretoken"]').val(),
            success: function (result) {
                if(result.delflag){
                    window.location.href='/login/'
                }

            }
        })
    });

    function search1(){
        //获取输入框内的值
        var search = $('#search').val();
        //简单的校验
        if (search.length < 4){
            alert('请输入不少于2个字符');
            return false;
        };
        if (!checkschool(search)){
            alert('数据库中暂无该学校相关信息')
            return false
        }
    }

    function checkschool(schoolname) {
    var flag = false;
    $.ajax({
        url:'/school/checkschool/',
        type:"GET",
        async:false,
        data:{'schoolname':schoolname},
        success: function (result) {
            var cflag = result.flag;
            if(cflag){
                flag = true;
            }
        }
    });
    return flag;
    }