<?php

require_once 'SqlHelper.class.php';

class EmpService{
    public function get_pagecount($page_size){
        $sqlHelper = new SqlHelper();
        $sql = "select count(id) from emp";
        $res = $sqlHelper->execute_sql($sql);
        if($row=mysql_fetch_row($res)){
            $row_count = $row[0];
        }
        $page_count = ceil($row_count/$page_size);
        mysql_free_result($res);
        $sqlHelper->close_connect();
        return $page_count;
    }

    public function get_res($page_now, $page_size){
        $sqlHelper = new SqlHelper();
        $sql = "select id, name, grade, email, salary from emp limit"
            .($page_now-1)*$page_size . ",$page_size";
        $res = $sqlHelper->execute_sql_arr($sql);
        $sqlHelper->close_connect();
        return $res;
    }

    public function get_page($page){
        $sqlHelper = new SqlHelper();
        $sql1 = "select id, name, grade, email, salary from emp limit ".
            ($page->page_now-1)*$page->page_size . ",$page->page_size";
        $sql2 = "select count(id) from emp";
        $sqlHelper->execute_sql_page($sql1, $sql2, $page);
        $sqlHelper->close_connect();
    }

    public function delete_by_id($id){
        $sqlHelper = new SqlHelper();
        $sql = "delete from emp where id=$id";
        $res =  $sqlHelper->execute_dml($sql) or die(mysql_error());
        $sqlHelper->close_connect;
        return $res;
    }

    public function add_emp($name, $grade, $email, $salary){
        $sqlHelper = new SqlHelper();
        $sql = "insert into emp(name, grade, email, salary) values ('$name', '$grade', '$email', '$salary')";
        $res = $sqlHelper->execute_dml($sql) or die(mysql_error);
        $sqlHelper->close_connect();
        return $res;
    }

    public function query_emp($id){
        $sqlHelper = new SqlHelper();
        $sql = "select * from emp where id=$id";
        $res =  $sqlHelper->execute_sql_arr($sql);
        $sqlHelper->close_connect();
        return $res;
    }

    public function update_emp($id, $name, $grade, $email, $salary){
        $sqlHelper = new SqlHelper();
        $sql = "update emp set name='$name', grade='$grade', email='$email', salary='$salary' where id=$id";
        $res = $sqlHelper->execute_dml($sql) or die(mysql_error);
        $sqlHelper->close_connect();
        //echo $res;
        return $res;
    }
}
