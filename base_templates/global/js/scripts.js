function my_scope() {
    const forms = document.querySelectorAll('.form-delete');

    for (form of forms){
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const confirmed = confirm('are you sure?');

            if(confirmed) {
                form.submit();
            }
        });
    }
}

my_scope();