import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.*;

public class webServiceRequest {
    
    public String sendGET(String request, String urlParameters) throws IOException{
        //String s1="test@hnelibrary.com";String s2="helloworld";
        //String urlParameters="email="+s1+"&password="+s2;            
        HttpURLConnection conn=null;
        //byte[] postData       = urlParameters.getBytes();
        //int    postDataLength = postData.length;
        //String request        = "http://127.0.0.1:5000/search";
        URL    url            = new URL( request );
        String Response="";
        try {      
            //Get and prepare specifications of connection to server
            conn= (HttpURLConnection) url.openConnection();           
           
            conn.setInstanceFollowRedirects( false );
            conn.setRequestMethod("GET");     
            conn.setRequestProperty( "Content-Type", "application/x-www-form-urlencoded");               
            String line="";                        
            InputStreamReader inputStreamReader=new InputStreamReader(conn.getInputStream()); //Get Response from server
            BufferedReader bufferedReader=new BufferedReader(inputStreamReader);
            StringBuilder response=new StringBuilder();             
            
            while ((line=bufferedReader.readLine())!=null){
                response.append(line); //storing in variable 'response'
            }
            bufferedReader.close();
            //Printing Response
            //System.out.println("Response :"+response.toString());
            Response=response.toString();
            
            }
            catch (Exception e){
                e.printStackTrace();
                //System.out.println("Error in Making POST Request");
            }
        finally{
            System.out.println("Response Code "+ conn.getResponseCode());
        }
        return Response;
        //System.out.println(Response);
        }
    



    public String sendPOST(String request, String urlParameters) throws IOException{
       // String s1="test@hnlibrary.com"; String s2="helloworld";
        //String urlParameters="email="+s1+"&password="+s2;            
            HttpURLConnection conn=null;
            byte[] postData       = urlParameters.getBytes();
            int    postDataLength = postData.length;
           // String request        = "http://127.0.0.1:5000/auth";
            URL    url            = new URL( request );
            String Response="";
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
            
            //Sending Data
            DataOutputStream wr = new DataOutputStream(conn.getOutputStream());
            wr.write( postData );            
            
            String line="";                        
            InputStreamReader inputStreamReader=new InputStreamReader(conn.getInputStream()); //Get Response from server
            BufferedReader bufferedReader=new BufferedReader(inputStreamReader);
            StringBuilder response=new StringBuilder();             
            
            while ((line=bufferedReader.readLine())!=null){
                response.append(line); //storing in variable 'response'
            }
            bufferedReader.close();
            //Printing Response
            //System.out.println("Response :"+response.toString());
            Response=response.toString();
            }
            catch (Exception e){
                e.printStackTrace();
                //System.out.println("Error in Making POST Request");
            }
        finally{
            System.out.println("Response Code "+ conn.getResponseCode());
        }
        return Response;
        }      
    
}
