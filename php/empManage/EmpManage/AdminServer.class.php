<?php

require_once 'SqlHelper.class.php';

class AdminServer{
    //checkout user legal
    public function check_user($username, $password){
        $sqlhelper = new SqlHelper();
        $sql = "select password, id from admin where name='" . $username."'";
        $res = $sqlhelper->execute_sql($sql);
        if($row=mysql_fetch_assoc($res)){
            if($row['password']==md5($password)){
                $id = $row['id'];
                return $id;
            }else{
                return null;
            }
        }else{
            return null;
        }
        //release
        mysql_free_result($res);
        //close connect
        $sqlhelper->close_connect();
    }

    public function update_logintime(){
        $sqlhelper = new SqlHelper();
        $sql = "update admin set login_time ='" .date("Y-m-d H:i:s")."'";
        $res = $sqlhelper->execute_sql($sql);
        $sqlhelper->close_connect();
    }

    public function get_lasttime(){
        /*
        */
        $sqlhelper = new SqlHelper();
        $sql = "select login_time from admin";
        $res = $sqlhelper->execute_sql($sql);
        $row=mysql_fetch_assoc($res);
        $sqlhelper->close_connect();
        return $row;
    }
}


