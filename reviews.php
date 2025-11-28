<?php
session_start();
if (!isset($_SESSION["role"])) {
    header("Location: index.php");
    exit();
}

?>

<!DOCTYPE html>
<html>
<head>
    <title>Reviews – AutoGrader AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="card">
        <h2>📨 Avis / Réclamations</h2>

        <p>Cette page affichera toutes les réclamations provenant des étudiants.</p>

        <p><i>(La fonctionnalité sera activée lorsque nous mettrons en place l'API /api/reviews)</i></p>

    </div>

</div>

<?php include "components/footer.php"; ?>

</body>
</html>
