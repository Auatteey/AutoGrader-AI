<?php
session_start();
if (!isset($_SESSION["role"])) {
    header("Location: index.php");
    exit();
}

$role = $_SESSION["role"];
$username = $_SESSION["username"];
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Reviews – AutoGrader AI</title>
    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="stylesheet" 
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>

<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="card">
        <h2 style="color: var(--accent); margin-bottom: 25px;">
            📨 Avis & Réclamations
        </h2>

        <?php if ($role === "etudiant"): ?>

            <!-- SECTION ÉTUDIANT : Formulaire d’envoi -->
            <p class="text-muted">Envoyez une réclamation concernant votre note.</p>

            <form action="data/reviews/submit_review.php" method="post" class="form-grid">

                <div>
                    <label>Examen concerné</label>
                    <select name="exam" required>
                        <option value="">-- Sélectionner --</option>

                        <?php
                        $exam_dir = __DIR__ . "/uploads/exams/";
                        foreach (scandir($exam_dir) as $exam) {
                            if ($exam !== "." && $exam !== "..") {
                                echo "<option>$exam</option>";
                            }
                        }
                        ?>
                    </select>
                </div>

                <div>
                    <label>Type de problème</label>
                    <select name="issue" required>
                        <option value="note">Note incorrecte</option>
                        <option value="feedback">Feedback incompréhensible</option>
                        <option value="ocr">Copie mal lue (OCR)</option>
                        <option value="bareme">Erreur dans le barème</option>
                        <option value="autre">Autre</option>
                    </select>
                </div>

                <div class="full-row">
                    <label>Description</label>
                    <textarea name="message" rows="6" 
                              placeholder="Expliquez votre problème..." required></textarea>
                </div>

                <button type="submit" class="btn-primary">
                    <i class="fa-solid fa-paper-plane"></i> Envoyer
                </button>
            </form>

        <?php else: ?>

            <!-- SECTION PROFESSEUR : Liste des réclamations -->
            <p class="text-muted">Voici toutes les réclamations envoyées par les étudiants :</p>

            <div class="reviews-list">

                <?php
                $reviews_path = __DIR__ . "/data/reviews/";
                $files = array_diff(scandir($reviews_path), ['.', '..']);

                if (empty($files)) {
                    echo "<p class='empty-info'>Aucune réclamation pour le moment.</p>";
                }

                foreach ($files as $file) {
                    $content = json_decode(file_get_contents($reviews_path . $file), true);

                    if (!$content) continue;

                    $student = htmlspecialchars($content["student"]);
                    $exam = htmlspecialchars($content["exam"]);
                    $issue = htmlspecialchars($content["issue"]);
                    $msg = nl2br(htmlspecialchars($content["message"]));
                    $date = htmlspecialchars($content["date"]);
                ?>

                    <div class="review-card">
                        <div class="review-header">
                            <i class="fa-solid fa-user-graduate"></i> 
                            <span><?= $student ?></span>
                        </div>

                        <div class="review-body">
                            <p><strong>Examen :</strong> <?= $exam ?></p>
                            <p><strong>Problème :</strong> <?= $issue ?></p>

                            <div class="review-message">
                                <?= $msg ?>
                            </div>

                            <p class="review-date">📅 <?= $date ?></p>
                        </div>

                        <div class="review-actions">
                            <button class="mini-btn">
                                <i class="fa-solid fa-reply"></i> Répondre
                            </button>

                            <button class="mini-btn danger">
                                <i class="fa-solid fa-trash"></i> Supprimer
                            </button>
                        </div>
                    </div>

                <?php } ?>
            </div>

        <?php endif; ?>

    </div>
</div>

<?php include "components/footer.php"; ?>

</body>
</html>
