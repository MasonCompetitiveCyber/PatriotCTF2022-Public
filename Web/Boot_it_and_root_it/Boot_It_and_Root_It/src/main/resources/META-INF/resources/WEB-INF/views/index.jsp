<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>
<html>

<head>
    <title>PCTF 2022</title>
    <link rel = "icon" href = "https://competitivecyber.club/images/mcc.ico">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

<style>
@import url(https://fonts.googleapis.com/css?family=Press+Start+2P);
@import url(https://fonts.googleapis.com/css?family=Fira+Mono:400);
html, body {
    height: 100%;
}

#backgroundCanvas {
    position: fixed;
    left: 0;
    top: 0;
    background-color: rgb(12, 26, 26);
    z-index: -1;
}

.form-signin {
    width: 100%;
    max-width: 330px;
    padding: 15px;
    margin: auto; 
}

.form-signin .form-floating:focus-within {
    z-index: 2;
}

/* .form-signin input[type="email"] {
margin-bottom: -1px;
border-bottom-right-radius: 0;
border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
margin-bottom: 10px;
border-top-left-radius: 0;
border-top-right-radius: 0;
} */

/* .form-control:valid {
    background-color:  black;
} */

#login-button {
    background-image: url("../static/imgs/static.gif");
}

h1 {
    animation: glitch 3s linear infinite;
    /* display: flex; */
    /* font-family: 'Fira Mono'; */
}

@keyframes glitch {
    2%, 20%, 38%, 70% {
        transform: translate(-1px, 0) skew(0deg);
    }
    10%, 44%, 60%, 75% {
        transform: translate(0px, 0) skew(0deg);
    }
    40% {
        transform: translate(1px, 1px) skew(8deg);
    }
    72% {
        transform: translate(1px, 1px) skew(-5deg);
    }
}

h1:before, h1:after {
    content: attr(title);
    position: absolute;
    left: 0;
}

h1:before {
    animation: glitchTop 1s linear infinite;
    clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
    -webkit-clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
}

@keyframes glitchTop {
    2%, 64% {
        transform: translate(2px, -2px);
    }
    4%, 60% {
        transform: translate(-2px, 2px);
    }
    62% {
        transform: translate(13px, -1px) skew(-53deg);
    }
}

h1:after {
    animation: glitchBottom 1.5s linear infinite;
    clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
    -webkit-clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
}

@keyframes glitchBottom {
    2%, 64% {
        transform: translate(-2px, 0);
    }
    4%, 60% {
        transform: translate(-2px, 0);
    }
    62% {
        transform: translate(-22px, 5px) skew(91deg);
    }
}

h1, h2 {
    color: white;
    font-family: 'Fira Mono', monospace;
}

.my-body {
    letter-spacing: -0.01em;
    /* font-family: 'Press Start 2P', cursive; */
    /* font-family: "Source Code Pro", monospace; */
    font-family: 'Fira Mono', monospace;
    /* justify-content: center; */
    /* text-shadow: 0px 0px 5px rgba(14, 87, 87, 0.83); */
    /* display: flex; */
    font-size: 1.003rem;
    /* background-color: rgb(12, 26, 26); */
    /* background: -webkit-gradient(linear, left top, left bottom, color-stop(0, #fff9ec), color-stop(90%, #fff));
    background: linear-gradient(to bottom, #fff9ec 0, #fff 90%); */
    /* cursor: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg'  width='40' height='48' viewport='0 0 100 100' style='fill:black;font-size:24px;'><text y='50%'>🍪</text></svg>"), auto */
}

/* @media (min-width: 769px) {
    .my-body {
        background: #300e3b url("https://www.dropbox.com/s/idu8lqyjba9fooa/back.png?raw=1") repeat 300% 300%;
        -webkit-animation: ScanLine 10s ease-in-out infinite;
        -moz-animation: ScanLine 10s ease-in-out infinite;
        animation: ScanLine 2s ease-in-out infinite;
    }
    @-webkit-keyframes ScanLine {
        0% {
            background-position: 51% 0%;
        }
        50% {
            background-position: 50% 100%;
        }
        100% {
            background-position: 51% 0%;
        }
    }
    @-moz-keyframes ScanLine {
        0% {
            background-position: 51% 0%;
        }
        50% {
            background-position: 50% 100%;
        }
        100% {
            background-position: 51% 0%;
        }
    }
    @keyframes ScanLine {
        0% {
            background-position: 51% 0%;
        }
        50% {
            background-position: 50% 100%;
        }
        100% {
            background-position: 51% 0%;
        }
    }
} */

/* .box {
    margin-top: 50px;
    margin-left: -2px;
    width: 100%;
} */

.border.blue {
    border: 2px solid #4BA0E3;
    -webkit-box-shadow: 0px 0px 4px 2px rgba(16, 81, 139, 0.78), inset 0px 0px 4px 2px rgba(16, 81, 139, 0.78);
    -moz-box-shadow: 0px 0px 4px 2px rgba(16, 81, 139, 0.78), inset 0px 0px 4px 2px rgba(16, 81, 139, 0.78);
    box-shadow: 0px 0px 4px 2px rgba(16, 81, 139, 0.78), inset 0px 0px 4px 2px rgba(16, 81, 139, 0.78);
}

.cursor {
    color: #93EDF5;
    background: transparent;
    text-shadow: 0px 0px 5px rgba(0, 255, 255, 0.83);
    opacity: 1;
    -webkit-animation: Blink 2s ease infinite;
    -moz-animation: Blink 2s ease infinite;
    animation: Blink 2s ease infinite;
}

@-webkit-keyframes Blink {
    0% {
        opacity: 0.5;
    }
    50% {
        opacity: 1;
    }
    100% {
        opacity: 0.5;
    }
}

@-moz-keyframes Blink {
    0% {
        opacity: 0.5;
    }
    50% {
        opacity: 1;
    }
    100% {
        opacity: 0.5;
    }
}

@keyframes Blink {
    0% {
        opacity: 0.5;
    }
    30%, 40%, 50%, 60%, 70% {
        opacity: 1;
    }
    100% {
        opacity: 0.5;
    }
}

/* body {
    font-size: .875rem;
} */

.feather {
    width: 16px;
    height: 16px;
    vertical-align: text-bottom;
}

/* main blockquote {
    position: relative;
    min-height: 130px;
    margin: 10px;
}

main blockquote .author {
    float: right;
}

main blockquote .warning {
    padding-top: 10px;
    text-align: center;
}

main blockquote .warning>span {
    color: black;
    background: #D4AFB9;
    font-weight: bold;
    text-transform: uppercase;
    text-shadow: none;
}

main .block {
    position: absolute;
    bottom: 15px;
} */

textarea {
    width: 100%;
    height: 100%;
    padding-left: 8px;
    padding-right: 8px;
    padding-top: 5px;
    padding-bottom: 5px;
    box-sizing: border-box;
    resize: none;
    background-color: transparent;
    border: none;
    outline: none;
    color: white;
    text-shadow: 2px 4px 4px gray;
    font-size: 1.0em;
    /* overflow: unset; */
    resize: none !important;
    caret-color: transparent;
}

.wrapper {
    padding: 2px;
    -webkit-animation: OpacityAnimation 10s ease-in-out infinite;
    -moz-animation: OpacityAnimation 10s ease-in-out infinite;
    animation: OpacityAnimation 10s ease-in-out infinite;
}

@-webkit-keyframes OpacityAnimation {
    0% {
        opacity: 0.8;
    }
    10% {
        opacity: 0.7;
    }
    20% {
        opacity: 0.9;
    }
    30% {
        opacity: 0.7;
    }
    40% {
        opacity: 0.9;
    }
    50% {
        opacity: 1;
    }
    60% {
        opacity: 0.9;
    }
    70% {
        opacity: 0.7;
    }
    80% {
        opacity: 0.9;
    }
    90% {
        opacity: 0.8;
    }
    100% {
        opacity: 0.9;
    }
}

@-moz-keyframes OpacityAnimation {
    0% {
        opacity: 0.8;
    }
    10% {
        opacity: 0.7;
    }
    20% {
        opacity: 0.9;
    }
    30% {
        opacity: 0.7;
    }
    40% {
        opacity: 0.9;
    }
    50% {
        opacity: 1;
    }
    60% {
        opacity: 0.9;
    }
    70% {
        opacity: 0.7;
    }
    80% {
        opacity: 0.9;
    }
    90% {
        opacity: 0.8;
    }
    100% {
        opacity: 0.9;
    }
}

@keyframes OpacityAnimation {
    0% {
        opacity: 0.8;
    }
    10% {
        opacity: 0.7;
    }
    20% {
        opacity: 0.9;
    }
    30% {
        opacity: 0.7;
    }
    40% {
        opacity: 0.9;
    }
    50% {
        opacity: 1;
    }
    60% {
        opacity: 0.9;
    }
    70% {
        opacity: 0.7;
    }
    80% {
        opacity: 0.9;
    }
    90% {
        opacity: 0.8;
    }
    100% {
        opacity: 0.9;
    }
}

#invalidChars {
    display: none;
    font-size: 0.8em;
}

#invalidChars.visible {
    display: block;
}
</style>
</head>

<body class="my-body text-center">
    <canvas class="background" id="backgroundCanvas"></canvas>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/particlesjs/2.2.3/particles.min.js"></script>
    <script>
        function canvas() {
            backgroundCanvas.width = window.innerWidth;
            backgroundCanvas.height = window.innerHeight;
        }

        canvas();
        Particles.init({
            selector: '.background',
            color: [
                "#006634",
                "#FFCC33",
            ],
            connectParticles: true,
        });
    </script>
    <div>
        <nav class="navbar fixed-top navbar-text bg-transparent">
    <div class="container-fluid d-flex justify-content-end">
        <li class="nav-item dropdown me-4">
            <a class="btn btn-lg btn-outline-info dropdown-toggle me-4" id="navbarDropdownMenuLink" role="button"
                data-bs-toggle="dropdown" aria-expanded="false" href="#">Hello</a>
            <ul class="dropdown-menu dropdown-menu-start mt-1 ms-4 dropdown-menu-dark"
                aria-labelledby="navbarDropdownMenuLink">
                <li>
                    <a class="dropdown-item" href="/">Send Message</a>
                </li>
                <li>
                    <a class="dropdown-item" href="#">Read Messages</a>
                </li>
                <li>
                    <form name="myform"  method="POST">
                        <button class="dropdown-item btn " type="submit">Clear Messages</button>
                    </form>
                </li>
                <li>
                    <hr class="dropdown-divider">
                </li>
                <li><a class="dropdown-item" href="#">Log Out</a></li>
            </ul>
        </li>
    </div>
</nav>


<div class="px-4 py-5 text-center">
    <h1>Secure Web App</h1>
    <h5 class="text-white">Trust me. It's very High and Hot</h5>
</div>

<div>
    <div class="form-signin">
        <form>
            <h2 class="h3 mb-3 fw-normal text-center text-capitalize">Please sign in</h2>
            <div class="mb-3">
                <input type="text" name="username" class="form-control" id="floatingInput" placeholder="Username">
            </div>
            <div class="mb-3">
                <input type="password" name="password" class="form-control" id="floatingPassword"
                    placeholder="Password">
            </div>
            <button class="w-100 btn btn-lg btn-dark" type="submit">Log In</button>
        </form>
        <form>
            <button class="w-100 mt-2 btn btn-sm btn-link" type="submit">Sign Up</button>
        </form>
    </div>
</div>

    </div>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"
        integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js"
        integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF"
        crossorigin="anonymous"></script>
    <script src="../static/main.js"></script>
</body>

</html>
