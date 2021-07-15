<script>

    var input = document.getElementById('namebucket');
    var form  = document.getElementById('form');

    input.oninvalid = function (event) {
        event.target.setCustomValidity('Username should only contain lowercase letters. e.g. john');
    }

    {/* var elem = document.createElement('div');
        elem.id = 'notify';
        elem.style.display = 'none';
        form.appendChild(elem);

        input.addEventListener('invalid', function (event) {
        event.preventDefault();
            if (!event.target.validity.valid) {
                elem.textContent = 'Username should only contain lowercase letters e.g. john';
                elem.className = 'error';
                elem.style.display = 'block';

                input.className = 'invalid animated shake';
                }
        });

    input.addEventListener('input', function (event) {
        if ('block' === elem.style.display) {
            input.className = '';
            elem.style.display = 'none';
            }
    }); */}

</script>