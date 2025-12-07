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
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Contacter le Professeur — AutoGrader AI</title>

    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <style>
        .contact-card {
            padding: 35px;
            background: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border-muted);
            box-shadow: var(--shadow);
            max-width: 700px;
            margin: 30px auto;
        }

        .contact-card h2 {
            color: var(--accent);
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .contact-card label {
            display: block;
            margin-top: 18px;
            margin-bottom: 5px;
            font-weight: 500;
            color: var(--text-light);
        }

        .contact-card select,
        .contact-card textarea {
            width: 100%;
            padding: 12px;
            background: var(--input-bg);
            border: 1px solid var(--border-muted);
            border-radius: 8px;
            color: var(--text-light);
            resize: none;
        }

        .contact-card textarea {
            height: 140px;
            margin-bottom: 10px;
        }

        .btn-primary {
            margin-top: 20px;
            width: 100%;
        }

        .contact-info {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-top: 15px;
            text-align: center;
        }
    </style>
</head>

<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="contact-card">

        <h2><i class="fa-solid fa-envelope-circle-check"></i> Contacter votre professeur</h2>

        <form method="post" action="reviews.php">

            <!-- EXAM CHOICE -->
            <label><i class="fa-solid fa-book"></i> Examen concerné</label>
            <select name="exam" required>
                <option value="">-- Sélectionnez un examen --</option>
                <?php
                foreach (scandir($exam_dir) as $exam) {
                    if ($exam !== "." && $exam !== ".." && is_dir($exam_dir . $exam)) {
                        echo "<option value='$exam'>$exam</option>";
                    }
                }
                ?>
            </select>

            <!-- PROBLEM TYPE -->
            <label><i class="fa-solid fa-circle-question"></i> Nature du problème</label>
            <select name="issue" required>
                <option value="">-- Sélectionnez --</option>
                <option>Note incorrecte</option>
                <option>Feedback incompréhensible</option>
                <option>Copie mal lue</option>
                <option>Erreur dans le barème</option>
                <option>Autre</option>
            </select>

            <!-- MESSAGE -->
            <label><i class="fa-solid fa-pen-to-square"></i> Description détaillée</label>
            <textarea name="message" placeholder="Expliquez clairement votre problème..." required></textarea>

            <button type="submit" class="btn-primary">
                <i class="fa-solid fa-paper-plane"></i> Envoyer la demande
            </button>

            <p class="contact-info">
                Votre professeur recevra automatiquement cette réclamation.<br>
                Une réponse apparaîtra dans la section <strong>Reviews</strong>.
            </p>

        </form>
    </div>

</div>

<?php include "components/footer.php"; ?>

</body>
</html>
