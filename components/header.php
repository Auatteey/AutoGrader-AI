<?php
if (!isset($_SESSION)) { session_start(); }
?>
<div class="header">

    <div class="header-left">
        <h1 class="app-title">AutoGrader AI</h1>
    </div>

    <div class="header-right">
        <?php if(isset($_SESSION["role"]) && $_SESSION["role"] === "etudiant"): ?>
            <a class="header-btn" href="contact.php">Contact Prof</a>
        <?php endif; ?>

        <?php if(isset($_SESSION["username"])): ?>
            <a class="header-btn logout-btn" href="logout.php">Logout</a>
        <?php endif; ?>
    </div>

</div>
