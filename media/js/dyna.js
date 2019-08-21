function passwordMatch()
{
    password = document.getElementById('password').value;
    confirm = document.getElementById('confirm').value;

    if(password != confirm) {
        document.getElementById('msg').innerHTML = 'not matching';
        document.getElementById('msg').style.color = 'red';

    } else {
        document.getElementById('msg').innerHTML = 'matching';
        document.getElementById('msg').style.color = 'green';
    }
}