<?php
session_start();
if($_SESSION['role']!="prof"){ header("Location:index.php"); exit(); }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Upload Exam — AutoGrader AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="container">
        <h2>Upload Exam</h2>

        <form action="upload_exam_handler.php" method="post" enctype="multipart/form-data">

            <label>Exam Name</label>
            <input type="text" name="exam_name" required>

            <label>Questions PDF</label>
            <input type="file" name="questions" required>

            <label>Correction PDF</label>
            <input type="file" name="correction" required>

            <label>Bareme PDF</label>
            <input type="file" name="bareme" required>

            <button type="submit">Upload</button>
        </form>
    </div>

</div>

<?php include "components/footer.php"; ?>

</body>
</html>
