<?php
session_start();
if (!isset($_SESSION["role"]) || $_SESSION["role"] !== "prof") {
    header("Location: index.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Uploader un Examen — AutoGrader AI</title>

    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>

<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="card upload-card">
        <h2><i class="fa-solid fa-file-circle-plus"></i> Uploader un Nouvel Examen</h2>

        <form method="post" action="upload_exam_handler.php" enctype="multipart/form-data" class="upload-form">

            <label>Nom de l’examen</label>
            <input type="text" name="exam_name" placeholder="Ex: prog_c" required>

            <!-- Questions PDF -->
            <label>Questions (PDF)</label>
            <label class="file-drop">
                <i class="fa-solid fa-file-arrow-up"></i>
                <p>Glisser-déposer ou cliquer</p>
                <input type="file" name="questions_pdf" accept="application/pdf" required>
            </label>

            <!-- Correction PDF -->
            <label>Correction (PDF)</label>
            <label class="file-drop">
                <i class="fa-solid fa-file-pen"></i>
                <p>Glisser-déposer ou cliquer</p>
                <input type="file" name="correction_pdf" accept="application/pdf" required>
            </label>

            <!-- Bareme PDF -->
            <label>Barème (PDF)</label>
            <label class="file-drop">
                <i class="fa-solid fa-scale-balanced"></i>
                <p>Glisser-déposer ou cliquer</p>
                <input type="file" name="bareme_pdf" accept="application/pdf" required>
            </label>

            <button class="btn-primary" type="submit">
                <i class="fa-solid fa-cloud-arrow-up"></i> Uploader l’examen
            </button>

        </form>
    </div>

</div>

<?php include "components/footer.php"; ?>
</body>
</html>
