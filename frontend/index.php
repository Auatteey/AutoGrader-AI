<?php
session_start();

if (isset($_POST['login'])) {
    $username = trim($_POST['username']);
    $role = $_POST['role'];

    $_SESSION['username'] = $username;
    $_SESSION['role'] = $role;

    if ($role === "prof") {
        header("Location: dashboard_prof.php");
    } else {
        header("Location: dashboard_etud.php");
    }
    exit();
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>AutoGrader AI – Connexion</title>

    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <style>
        /* --- LOGIN WRAPPER --- */
        .login-wrapper {
            display: flex;
            height: calc(100vh - 120px);
            justify-content: center;
            align-items: center;
            padding-top: 40px;
        }

        .login-container {
            background: var(--card-bg);
            border-radius: 14px;
            padding: 40px 45px;
            width: 420px;
            border: 1px solid var(--border-muted);
            box-shadow: var(--shadow-xl);
            animation: fadeIn 0.6s ease forwards;
        }

        .login-container h2 {
            color: var(--accent);
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
        }

        .login-container label {
            display: block;
            margin-top: 15px;
            margin-bottom: 5px;
            font-weight: 500;
            color: var(--text-light);
        }

        .login-container input,
        .login-container select {
            width: 100%;
            padding: 12px;
            background: var(--input-bg);
            border: 1px solid var(--border-muted);
            border-radius: 8px;
            color: var(--text-light);
            margin-bottom: 5px;
        }

        .login-container input:focus,
        .login-container select:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 6px var(--accent-soft);
        }

        .login-btn {
            width: 100%;
            margin-top: 20px;
        }

        /* Fade-in animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .login-info {
            text-align: center;
            color: var(--text-muted);
            margin-top: 15px;
            font-size: 0.85rem;
        }

    </style>
</head>

<body>

<?php include "components/header.php"; ?>

<div class="login-wrapper">
    <div class="login-container">
        <h2><i class="fa-solid fa-right-to-bracket"></i> Connexion</h2>

        <form method="post">

            <!-- Username -->
            <label><i class="fa-solid fa-user"></i> Nom d'utilisateur</label>
            <input type="text" name="username" placeholder="Entrez votre nom..." required>

            <!-- Role -->
            <label><i class="fa-solid fa-users"></i> Rôle</label>
            <select name="role" required>
                <option value="">-- Sélectionner --</option>
                <option value="prof">Professeur</option>
                <option value="etudiant">Étudiant</option>
            </select>

            <!-- Login Button -->
            <button type="submit" name="login" class="btn-primary login-btn">
                <i class="fa-solid fa-arrow-right-to-bracket"></i> Se connecter
            </button>

            <p class="login-info">
                Accédez à votre espace personnalisé pour gérer ou soumettre vos examens.
            </p>

        </form>
    </div>
</div>

<?php include "components/footer.php"; ?>

</body>
</html>
