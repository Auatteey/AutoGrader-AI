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
<html>
<head>
    <title>AutoGrader AI – Login</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<?php include "components/header.php"; ?>

<div class="login-wrapper">
    <div class="container login-container">
        <h2>🔒 Connexion</h2>

        <form method="post">
            <label>Nom d'utilisateur</label>
            <input type="text" name="username" placeholder="Entrez votre nom..." required>

            <label>Rôle</label>
            <select name="role" required>
                <option value="prof">Professeur</option>
                <option value="etudiant">Étudiant</option>
            </select>

            <button type="submit" name="login">Se connecter</button>
        </form>
    </div>
</div>


<?php include "components/footer.php"; ?>

</body>
</html>
