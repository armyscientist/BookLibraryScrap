import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.*;

public class HttpClientAuthenticate2 {
    
    public static void main(String[] args) throws IOException{
        //String s1="test@hnelibrary.com";
        //String s2="helloworld";


        String urlParameters="membername=Amruta  Yemul&email=yemulaj18@gmail.com&password=youngforever&mobile=9405895281&gender=F&address=107,Sakhar Peth&city=Solapur&age=20&occupation=Student";            
            HttpURLConnection conn=null;
            byte[] postData       = urlParameters.getBytes();
            int    postDataLength = postData.length;
            String request        = "http://127.0.0.1:5000/register";
            URL    url            = new URL( request );
            
        try {
            
            //Get and prepare specifications of connection to server
            conn= (HttpURLConnection)url.openConnection();           
            conn.setDoOutput( true );
            conn.setInstanceFollowRedirects( false );
            conn.setRequestMethod( "POST" );
            
            conn.setRequestProperty( "Content-Type", "application/x-www-form-urlencoded"); 
            conn.setRequestProperty( "charset", "utf-8");
            conn.setRequestProperty( "Content-Length", Integer.toString( postDataLength ));
            conn.setUseCaches( false );
            //System.out.println("******************Sending");
            //Sending Data
            DataOutputStream wr = new DataOutputStream(conn.getOutputStream());
            wr.write( postData );
            //System.out.println("******************Writing");
            
            String line="";                        
            InputStreamReader inputStreamReader=new InputStreamReader(conn.getInputStream()); //Get Response from server
            BufferedReader bufferedReader=new BufferedReader(inputStreamReader);
            StringBuilder response=new StringBuilder();             
            //System.out.println("************Receiving");
            while ((line=bufferedReader.readLine())!=null){
                response.append(line); //storing in variable 'response'
            }
            bufferedReader.close();
            //Printing Response
            System.out.println("Response :"+response.toString());
            
            }
            catch (Exception e){
                e.printStackTrace();
                System.out.println("Error in Making POST Request");
            }
        finally{
            System.out.println("Response Code "+ conn.getResponseCode());
        }
        
    }
}
