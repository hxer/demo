<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
</head>
<?php
    require_once 'EmpService.class.php';
    require_once 'Page.class.php';
    require_once 'common.php';

    $page = new Page();
    $page->page_now=1;
    if(!empty($_GET['page'])){
        $page->page_now = $_GET['page'];
    }
    $page->page_count = 0;
    $page->page_size = 5;
    $page->row_count = 0;
    $page->goto_url = "list_emp.php";

    $emp_service = new EmpService();
    $emp_service->get_page($page);
    echo "<table border='1px' >";
    echo "<tr><th>id</th><th>name</th><th>grade</th><th>email</th><th>salary</th>
        <th><a href='#'>删除用户</a></th><th><a href='#'>修改用户</a></th></tr>";
    for($i=0; $i<count($page->res_array); $i++){
        $row = $page->res_array[$i];
        echo "<tr><th>{$row['id']}</th><th>{$row['name']}</th><th>{$row['grade']}</th>
            <th>{$row['email']}</th><th>{$row['salary']}</th><th>
            <a href='process_emp.php?flag=del&id={$row['id']}'>删除用户</a></th>
            <th><a href='update_emp.php?flag=update&id={$row['id']}&name={$row['name']}&grade={$row['grade']}&email={$row['email']}&salary={$row['salary']}'>修改用户</a></th></tr>";
    }
    echo "</table>";
    echo "$page->page_jump";
    echo "<a href='main.php'>返回主页</a>";
?>
</html>
