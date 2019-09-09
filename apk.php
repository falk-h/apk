<!DOCTYPE html>
<html>
<head>
    <title>APK</title>
    <meta charset="utf-8" />
    <link rel="icon" href="/favicon.png" />
    <link href='https://fonts.googleapis.com/css?family=Aguafina Script' rel='stylesheet' />
    <style type="text/css">
        body {
            margin: 40px auto;
            max-width: 100%;
            line-height: 1.6;
            background-color: #EEEEEE;
            padding: 0 10px;
            font-family: Helvetica, Arial, sans-serif;
        }

        h1 {
            color: #002244;
            line-height: 1;
            font-size: 96px;
            font-family: 'Aguafina Script', sans-serif;
            text-decoration: underline;
        }

        h2 {
            color: #002244;
            line-height: 0.3;
            font-size: 72px;
            font-family: 'Aguafina Script', sans-serif;
            text-decoration: underline;
            transform: translateY(100%);
        }
        a {
                cursor: pointer;
        }

        table {
            margin-left:auto;
            margin-right:auto;
            max-width: 100%;
        }

        .id {
            text-align: left;
            font-weight: bold;
        }
    </style>
</head>
<body>
        <div style="margin-left:auto; margin-right:auto;">
                <center>
                        <h1>APK!</h1>
                        APK räknas ut som milliliter ren alkohol per krona, inklusive pant, för vem pallar panta?<br />
                        Exkluderar förhoppningsvis dricka utan alkohol, lokalt och småskaligt, och beställningsvaror.<br />
                        Systemet förklarar inte vad kategorierna i API:t betyder, så vissa sådana grejer kanske finns med ändå. ¯\_(ツ)_/¯<br />
                        Uppdateras automatiskt via <a href="https://www.systembolaget.se/api">Systemets API</a> varje natt.<br />
                        Listorna med basendricka anger vad drickan hade kostat om den hade sålts i Basen.<br />
                        <?php
                        include 'apk_raw.html';
                        ?>
                </center>
        </div>
</body>
</html>
