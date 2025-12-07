<?php
session_start();
if (!isset($_SESSION["role"]) || $_SESSION["role"] !== "etudiant") {
    header("Location: index.php");
    exit();
}

$username = $_SESSION["username"];
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Soumettre ma Copie — AutoGrader AI</title>

    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>

<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="card upload-card">
        <h2><i class="fa-solid fa-file-upload"></i> Soumettre ma Copie</h2>

        <form method="post" action="upload_copy_handler.php"
              enctype="multipart/form-data" class="upload-form">

            <label>Choisir l'examen</label>
            <select name="exam_name" required class="input-select">
                <option value="" disabled selected>-- Sélectionner --</option>
                <?php
                foreach (scandir("uploads/exams") as $exam) {
                    if ($exam !== "." && $exam !== "..")
                        echo "<option value='$exam'>$exam</option>";
                }
                ?>
            </select>

            <label>Votre copie (PDF uniquement)</label>

            <label class="file-drop">
                <i class="fa-solid fa-file-import"></i>
                <p>Glisser-déposer ou cliquer</p>
                <input type="file" name="copy_file" accept="application/pdf" required>
            </label>

            <button class="btn-primary" type="submit">
                <i class="fa-solid fa-paper-plane"></i> Envoyer la copie
            </button>

        </form>
    </div>

</div>

<?php include "components/footer.php"; ?>
</body>
</html>
