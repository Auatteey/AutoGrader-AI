<?php
session_start();
if (!isset($_SESSION["role"]) || $_SESSION["role"] !== "etudiant") {
    header("Location: index.php");
    exit();
}

$username = $_SESSION["username"];
$exam_dir = __DIR__ . "/uploads/exams/";
?>

<!DOCTYPE html>
<html>
<head>
    <title>Contact Prof – AutoGrader AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<?php include "components/header.php"; ?>


<div class="main-content">
    <div class="card">
        <h2>✉️ Contacter votre professeur</h2>

        <form method="post" action="reviews.php">

            <label>Examen concerné</label>
            <select name="exam" required>
                <option value="">-- Sélectionnez --</option>
                <?php
                foreach (scandir($exam_dir) as $exam) {
                    if ($exam !== "." && $exam !== "..")
                        echo "<option value='$exam'>$exam</option>";
                }
                ?>
            </select>

            <label>Nature du problème</label>
            <select name="issue" required>
                <option>Note incorrecte</option>
                <option>Feedback incompréhensible</option>
                <option>Copie mal lue</option>
                <option>Erreur dans le barème</option>
                <option>Autre</option>
            </select>

            <label>Description détaillée</label>
            <textarea name="message" rows="6" required></textarea>

            <button type="submit">Envoyer</button>

        </form>
    </div>
</div>

<?php include "components/footer.php"; ?>
</body>
</html>
