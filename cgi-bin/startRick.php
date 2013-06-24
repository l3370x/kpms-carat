<?PHP
$mysqli = new mysqli("db475444103.db.1and1.com", "dbo475444103", "calm1717", "db475444103");

$mysqli->query('insert into teacher_teacher values(1,2,"Richard","Miller","rick@calmriver.com")');

$mysqli->close();
?>
