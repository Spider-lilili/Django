//邮箱判断
function isEmail(str) {
    var reg = /^[a-zA-Z0-9_-]{6,}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
    return reg.test(str);
}

//判断用户名是否已存在（登陆验证）
function checkname(username) {
    var flag = false;
    $.ajax({
        url:'/checkname/',
        type:"GET",
        async:false,
        data:{'uname':username},
        success: function (result) {
            var cflag = result.flag;
            if(cflag){
                flag = true;
                $('#aSpan').html('用户名已存在！')
            }
            else{
                $('#aSpan').html('')
            }

        }
    });
    return flag;
}

// 验证登陆登陆是否成功
function verifylogin(user_name, password) {
    var cflag = false;
    $.ajax({
        url:'/verifypassword/',
        type:'get',
        data:{'username':user_name, 'password':password},
        async:false,
        success:function(result){
            var flag = result.checkFlag;
            if(flag){
                cflag = true;
            }

        }
    });

    return cflag;
}

// 注册验证
function register1(){
    //获取输入框内的值
    var account = $('#user_name').val();
    var password = $('#user_password').val();
    var email = $('#user_email').val();
    //简单的校验
    if(account.length<4||checkname(account)){
        $('#aSpan').text('用户名不能小于四位！');
        return false;
    }
    if(!isEmail(email)){
        $('#eSpan').text('邮箱格式不规范！');
        return false;
    }

    if(password.length<6){
        $('#pSpan').text('密码长度不能小于六位');
        return false;
    }

    //将密码进行加密
    var hex_pwd = hex_md5(password);
    $('#user_password').val(hex_pwd);
    return true;
    }

function changecode(imgObj) {
    imgObj.src = '/loadcode/?time='+ new Date().getTime();
}

function login1(){
    var user_name = $('#username').val();
    //获取输入框的值
    var password = $('#pwd').val();
    //简单校验
    // var code = $('#code').val();
    // var cflag = checkCode(code);
    // if(!cflag){
    //     $('#cSpan').text('×');
    //     return false;
    // }
    var hex_pwd = hex_md5(password);
    $('#pwd').val(hex_pwd);
    if(verifylogin(user_name,hex_pwd)){
        return true;
    }
    else{
        $('#pSpan').text('密码错误!!!');
        alert('密码错误!!!')
        return false;
    }
}

function checkCode(txt){
    var cflag = false;
    $.ajax({
        url:'/checkcode/',
        type:'get',
        data:{'code':txt},
        async:false,
        success:function(result){
            var flag = result.checkFlag;
            if(flag){
                cflag = true;
                $('#cSpan').text('√');
            }else{
                $('#cSpan').text('×');
            }
        }
    });
    return cflag;
};


// 忘记密码邮箱验证
function ReceiveEmail() {
    var user = $('#user_name').val();
    var email = $('#email').val();
    // 验证用户是否注册
    if(!checkname(user)){
        $('#aSpan').text('该用户名不存在！');
        return false;
    }
    else{
        $('#aSpan').html('')
    }
    // 验证邮箱格式是否规范
    if(!isEmail(email)){
        $('#pSpan').text('邮箱格式不规范！');
        return false;
    }
    else{
        $('#pSpan').html('')
    }

}

// 验证修改两次密码是否一致
function verifypassword() {
    // $('#password').val('');
    // $('#password1').val('');
    var password = $('#password').val();
    var password1 = $('#password1').val();
    var flag = false;
    if(password == password1){
        flag = true;
    }
    else{
        $('#pSpan').html('两次密码不一致！');

    }
    if(password.length<6){
        $('#pSpan').text('密码长度不能小于六位');
        return false;
    }
    var hex_pwd = hex_md5(password);
    $('#password').val(hex_pwd);
    var hex_pwd1 = hex_md5(password1);
    $('#password1').val(hex_pwd1);
    return flag;
}
