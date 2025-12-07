<?php 
session_start();
if (!isset($_SESSION["role"]) || $_SESSION["role"] !== "prof") {
    header("Location: index.php");
    exit();
}

$exam_dir = __DIR__ . "/uploads/exams/";
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Professeur – AutoGrader AI</title>
    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>

<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <!-- ============================
         UPLOAD EXAM AREA
    =============================== -->
    <div class="card">
        <h2 style="color: var(--accent); margin-bottom: 20px;">
            📥 Importer un examen
        </h2>

        <form action="upload_exam.php" method="post" enctype="multipart/form-data">

            <label>Nom de l'examen :</label>
            <input type="text" name="exam_name" placeholder="ex: algo_2025" required>

            <label>Questions (PDF)</label>  <br> <br>
           <label class="ai-file-upload" style="
                border: 2px dashed #30363d;
                padding: 25px;
                text-align: center;
                display: block;
                border-radius: var(--radius);
                cursor: pointer;
                transition: .2s;
                background: var(--bg-secondary);
            "> 
                <i class="fa-solid fa-cloud-arrow-up" style="font-size: 40px; color: var(--accent);"></i>
                <p style="margin-top: 10px; color: var(--text-secondary);">Glisser-déposer votre examen </p>
                <span class="browse" style="color: var(--accent); font-weight: 600;">Choisir un fichier</span>
                <input type="file" name="copy" accept="application/pdf" required
                    style="opacity: 0; position: absolute; width: 100%; height: 100%; cursor: pointer;">
            </label>

            <label>Correction (PDF)</label>  <br> <br>
            <label class="ai-file-upload" style="
                border: 2px dashed #30363d;
                padding: 25px;
                text-align: center;
                display: block;
                border-radius: var(--radius);
                cursor: pointer;
                transition: .2s;
                background: var(--bg-secondary);
            "> 
                <i class="fa-solid fa-cloud-arrow-up" style="font-size: 40px; color: var(--accent);"></i>
                <p style="margin-top: 10px; color: var(--text-secondary);">Glisser-déposer votre correction </p>
                <span class="browse" style="color: var(--accent); font-weight: 600;">Choisir un fichier</span>
                <input type="file" name="copy" accept="application/pdf" required
                    style="opacity: 0; position: absolute; width: 100%; height: 100%; cursor: pointer;">
            </label>
 <label>baréme (PDF)</label> <br> <br>
              <label class="ai-file-upload" style="
                border: 2px dashed #30363d;
                padding: 25px;
                text-align: center;
                display: block;
                border-radius: var(--radius);
                cursor: pointer;
                transition: .2s;
                background: var(--bg-secondary);
            "> 
                <i class="fa-solid fa-cloud-arrow-up" style="font-size: 40px; color: var(--accent);"></i>
                <p style="margin-top: 10px; color: var(--text-secondary);">Glisser-déposer votre baréme </p>
                <span class="browse" style="color: var(--accent); font-weight: 600;">Choisir un fichier</span>
                <input type="file" name="copy" accept="application/pdf" required
                    style="opacity: 0; position: absolute; width: 100%; height: 100%; cursor: pointer;">
            </label>

            <button type="submit">Uploader l'examen</button>
        </form>
    </div>


    <!-- ============================
         LIST OF UPLOADED EXAMS
    =============================== -->
    <div class="card">
        <h2 style="color: var(--accent); margin-bottom: 20px;">
            📂 Examens enregistrés
        </h2>

        <table>
            <tr>
                <th>Examen</th>
                <th>Questions</th>
                <th>Correction</th>
                <th>Barème</th>
                <th>Actions</th>
            </tr>

            <?php
            foreach (scandir($exam_dir) as $exam) {
                if ($exam === "." || $exam === "..") continue;

                $path = $exam_dir . $exam . "/";

                if (!is_dir($path)) continue;

                $q = file_exists($path . "questions.pdf");
                $c = file_exists($path . "correction.pdf");
                $b = file_exists($path . "bareme.pdf");

                echo "<tr>
                    <td><strong style='color:var(--accent)'>$exam</strong></td>

                    <td>" . ($q ? "<a href='$path/questions.pdf' target='_blank'>Voir</a>" : "—") . "</td>
                    <td>" . ($c ? "<a href='$path/correction.pdf' target='_blank'>Voir</a>" : "—") . "</td>
                    <td>" . ($b ? "<a href='$path/bareme.pdf' target='_blank'>Voir</a>" : "—") . "</td>

                    <td>
                        <button class='mini-btn' onclick=\"location.href='results.php?exam=$exam'\">
                            <i class='fa-solid fa-chart-column'></i>
                        </button>

                        <button class='mini-btn danger' onclick=\"alert('⚠️ Supprimer sera possible après ajout DB')\">
                            <i class='fa-solid fa-trash'></i>
                        </button>
                    </td>
                </tr>";
            }
            ?>
        </table>

    </div>

</div>

<?php include "components/footer.php"; ?>

</body>
</html>
