<?php
/*
mysql> describe admin; admin admin123
+------------+------------------+------+-----+-------------------+-----------------------------+
| Field      | Type             | Null | Key | Default           | Extra                       |
+------------+------------------+------+-----+-------------------+-----------------------------+
| id         | int(10) unsigned | NO   | PRI | NULL              |                             |
| name       | varchar(32)      | NO   |     | NULL              |                             |
| password   | varchar(128)     | NO   |     | NULL              |                             |
| login_time | timestamp        | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
+------------+------------------+------+-----+-------------------+-----------------------------+


mysql> describe emp;
+--------+------------------+------+-----+---------+----------------+
| Field  | Type             | Null | Key | Default | Extra          |
+--------+------------------+------+-----+---------+----------------+
| id     | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| name   | varchar(64)      | NO   |     | NULL    |                |
| grade  | tinyint(4)       | NO   |     | NULL    |                |
| email  | varchar(128)     | NO   |     | NULL    |                |
| salary | float            | NO   |     | NULL    |                |
+--------+------------------+------+-----+---------+----------------+

*/


class SqlHelper{
    public $conn;
    public $dbname="empmanage";
    public $host="localhost";
    public $username="phper";
    public $password="phpdb";

    public function __construct(){
        $conn = mysql_connect($this->host, $this->username, $this->password);
        if(!$conn) {
            die("connect error:".mysql_error());
        }
        mysql_select_db($this->dbname) or die(mysql_error());
        //mysql_query("set names utf-8", $this->conn);
    }

    public function execute_sql($sql){
        $res = mysql_query($sql) or die(mysql_error());
        return $res;
    }

    public function execute_sql_arr($sql){
        /*
        return a array
        */
        $arr = array();
        $i = 0;
        $res = mysql_query($sql) or die(mysql_error());
        while($row=mysql_fetch_assoc($res)){
            $arr[$i++] = $row;
        }
        mysql_free_result($res);
        return $arr;
    }

    public function execute_sql_page($sql1, $sql2, $page){
        /*
        */
        $res = mysql_query($sql1) or die(mysql_error());
        $arr = array();
        while($row=mysql_fetch_assoc($res)){
            $arr[] = $row;
        }
        mysql_free_result($res);
        $page->res_array=$arr;

        $res2 = mysql_query($sql2) or die(mysql_error());
        if($row=mysql_fetch_row($res2)){
            $page->row_count = $row[0];
            $page->page_count = ceil($row[0]/$page->page_size);
        }
        mysql_free_result($res2);

        $pagejump = "";
        if($page->page_now > 1){
            $pre_page = $page->page_now - 1;
            $page->pagejump = "<a href='{$page->goto_url}?page=$pre_page'>上一页</a>";
        }
        if($page->page_now < $page->page_count){
            $next_page = $page->page_now + 1;
            $page->pagejump .= "<a href='{$page->goto_url}?page=$next_page'>下一页</a>";
        }
        //print
        $start = floor(($page->page_now-1)/10)*10+1;
        $index = $start;
        if($page->page_now > 10){
            $page->pagejump .= "<a href='{$page->goto_url}?page" .($start-1). "'><<</a>";
        }
        for(; $start<$index+10; $start++){
            $page->page_jump .= "<a href='{$page->goto_url}?page=$start'>[$start]</a>";
        }
        $page->page_jump .= "  <a href='{$page->goto_url}?page=$start'>>></a>";
        $page->page_jump .= "   当前{$page->page_now}页/共{$page->page_count}页";
    }

    public function execute_dml($sql){
        //echo $sql;
        $res = mysql_query($sql) or die(mysql_error());
        if(!$res){
            return 0;   //no user match
        }
        if(mysql_affected_rows() > 0){
            return 1;   //ok
        }else{
            return 2;
        }
    }

    public function close_connect(){
        if(!empty($this->conn)){
            mysql_close($this->conn);
        }
    }
}
