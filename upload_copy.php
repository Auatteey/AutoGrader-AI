<?php
session_start();
if($_SESSION['role']!="etudiant"){ header("Location:index.php"); exit(); }
$username=$_SESSION['username'];
?>

<!DOCTYPE html>
<html>
<head>
    <title>Upload Your Copy — AutoGrader AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="container">
        <h2>Upload Your Copy</h2>

        <form action="upload_copy_handler.php" method="post" enctype="multipart/form-data">

            <label>Select Exam</label>
            <select name="exam_name" required>
                <?php foreach(scandir("uploads/exams") as $e){ if($e!="." && $e!="..") echo "<option>$e</option>"; } ?>
            </select>

            <label>Choose your file</label>
            <input type="file" name="copy_file" required>

            <button type="submit">Upload</button>
        </form>
    </div>

</div>

<?php include "components/footer.php"; ?>

</body>
</html>
