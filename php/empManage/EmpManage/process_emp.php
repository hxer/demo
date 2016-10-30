<?php

require_once 'EmpService.class.php';
require_once 'Emp.class.php';

$emp_service = new EmpService();
if(!empty($_REQUEST['flag'])){
    if($_REQUEST['flag'] == 'del'){
        $id = $_REQUEST['id'];
        if($emp_service->delete_by_id($id) == 1){
            header("Location:ok.php");
            exit();
        }else{
            header("Location:err.php");
            exit();
        }
    }else if($_REQUEST['flag'] == 'add_emp'){
        $name = $_REQUEST['name'];
        $grade = $_REQUEST['grade'];
        $email = $_REQUEST['email'];
        $salary = $_REQUEST['salary'];
        if($emp_service->add_emp($name, $grade, $email, $salary) == 1){
            header("Location:ok.php");
            exit();
        }else{
            header("Location:err.php");
            exit();
        }
    }else if($_REQUEST['flag'] == 'update_emp'){
        $id  = $_REQUEST['id'];
        $name = $_REQUEST['name'];
        $grade = $_REQUEST['grade'];
        $email = $_REQUEST['email'];
        $salary = $_REQUEST['salary'];
        if($emp_service->update_emp($id, $name, $grade, $email, $salary) == 1){
            header("Location:ok.php");
            exit();
        }else{
            header("Location:err.php");
            exit();
        }
    }else if($_REQUEST['flag'] == 'query_emp'){
        if(!empty($_REQUEST['id'])){
            $id = $_REQUEST['id'];
            if($res=$emp_service->query_emp($id)){
                echo "id:{$res[0]['id']}<br/> name:{$res[0]['name']}<br/> grade:{$res[0]['grade']}<br/>
                    email:{$res[0]['email']}<br/> salary:{$res[0]['salary']}<br/>";
            }else{
                echo "用户不存在<br/>";
                echo "<a href='query_emp.php'>返回查询</a><br/>";
                echo "<a href='main.php'>返回主页</a><br/>";
            }
        }else{
            echo "请输入用户id<br/>";
            echo "<a href='query_emp.php'>返回查询</a><br/>";
            echo "<a href='main.php'>返回主页</a><br/>";
        }
    }
}
