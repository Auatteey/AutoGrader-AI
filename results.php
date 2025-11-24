<?php
session_start();
if(!isset($_SESSION['role']) || $_SESSION['role'] != "etudiant"){
    header("Location: index.php");
    exit();
}
$username = $_SESSION['username'];
?>

<!DOCTYPE html>
<html>
<head>
    <title>Résultats Étudiant</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">
    <h2>Résultats pour <?php echo htmlspecialchars($username); ?></h2>
    <a href="dashboard_etud.php">Retour</a>

    <table border="1">
        <tr>
            <th>Examen</th>
            <th>Note</th>
            <th>Feedback</th>
        </tr>
        <?php
        // À remplacer par la lecture des fichiers JSON/csv générés par FastAPI
        echo "<tr><td>Examen 1</td><td>8/20</td><td>Bonne réponse mais incomplète</td></tr>";
        echo "<tr><td>Examen 2</td><td>6/20</td><td>Revoir certaines notions</td></tr>";
        ?>
    </table>
</div>
</body>
</html>
