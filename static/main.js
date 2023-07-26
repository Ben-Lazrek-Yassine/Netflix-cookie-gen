const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer);
        toast.addEventListener('mouseleave', Swal.resumeTimer);
    }
});


function showGeneratedData(generatedAccount) {
    var generatedAccountTextarea = document.getElementById("cookies"); // Use the correct ID "cookies"
    generatedAccountTextarea.value = generatedAccount;
    $("#generatedData").show();
    $("#copyProxiesBtn").show();
    $("#copyCookiesBtn").show();
    $("#copyGeneratedBtn").show();
}

// The rest of the code remains unchanged

$('#genbtn').click(function () {
    var name = document.getElementById("gen").value;
    var genbtn = document.getElementById("genbtn");
    if (name === "disabled") {
        genbtn.disabled = true;
        Swal.fire({
            icon: 'info',
            text: 'Select a gen from the dropdown menu'
        });
    } else {
        r = new XMLHttpRequest();
        r.open("GET", "/gen?name=" + name, "True");
        r.send();
        r.onload = function () {
            if (r.status === 200) {
                var generatedAccount = r.responseText; 
                Swal.fire({
                    title: "Successfully Generated Account and copied to clipboard",
                    icon: "success",
                    confirmButtonColor: "#4f4f4f",
                });
                showGeneratedData(generatedAccount);
            } else if (r.status === 202) {
                genbtn.disabled = true;
                Swal.fire({
                    icon: 'warning',
                    text: 'That gen type is out of stock'
                });
            } else if (r.status === 404) {
                genbtn.disabled = true;
                Swal.fire({
                    icon: 'error',
                    text: 'That gen type does not exist'
                });
            } else if (r.status === 429) {
                Swal.fire({
                    icon: 'error',
                    text: 'Wait at least 5 seconds before generating another account!'
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    text: 'An error occurred'
                });
            }
        };
    }
});
function copyToClipboard(text) {
    if (navigator.clipboard) {
        // Use the newer clipboard.writeText method (preferred)
        navigator.clipboard.writeText(text)
            .then(() => {
                // Show a success toast notification
                Toast.fire({
                    icon: 'success',
                    title: 'Cookie copied to clipboard'
                });
            })
            .catch((err) => {
                // Show an error toast notification if the copy operation fails
                Toast.fire({
                    icon: 'error',
                    title: 'Failed to copy cookie to clipboard'
                });
            });
    } else {
        // For older browsers that don't support the Clipboard API
        var textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        // Show a success toast notification
        Toast.fire({
            icon: 'success',
            title: 'Cookie copied to clipboard'
        });
    }
}
$('#gen').change(function () {
    var name = $(this).val();
    if (name === "cookie") {
        r = new XMLHttpRequest();
        r.open("GET", "/load_cookie_json", "True");
        r.send();
        r.onload = function () {
            if (r.status === 200) {
                var cookieJson = r.responseText;
                try {
                    var cookie = JSON.parse(cookieJson); // Parse the JSON string
                    $("#cookie").val(cookie); // Set the value of the textarea
                } catch (error) {
                    Swal.fire({
                        icon: 'error',
                        text: 'Error parsing JSON cookie'
                    });
                }
            }
        };
    } else {
        $("#cookie").val("");
    }
});


$('#copyCookieBtn').click(function () {
    var generatedAccountTextarea = document.getElementById("cookies");
    var generatedAccount = generatedAccountTextarea.value;
    copyToClipboard(generatedAccount);
});

window.onload = function () {
    document.getElementById("cookies").value = "";
};